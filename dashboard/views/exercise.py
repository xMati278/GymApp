from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from trainings.models import Exercise, BodyPart, UserTrainingPlans, TrainingPlanExerciseInfo
from django.http import Http404
from trainings.forms import ExerciseForm, CreateExerciseForm, AddExerciseToPlanForm
from dashboard.mixins import ExercisesOwnerRequiredMixin
from django.db.models import Q



class ExercisesView(ListView):
    template_name = 'dashboard/exercises.html'
    paginate_by = 10
    model = Exercise
    queryset = Exercise.objects.all()

    def fetch_query_params(self) -> tuple[str, str, str]:
        search_query = self.request.GET.get('search', '')
        sort_by = self.request.GET.get('sort_by', '')
        body_part_filter = self.request.GET.get('body_part', '')

        return search_query, sort_by, body_part_filter

    def get_queryset(self):
        search_query, sort_by, body_part_filter = self.fetch_query_params()
        queryset = self.queryset
        queryset = queryset.filter(
            Q(public=True) | Q(public=False, user=self.request.user)
        )

        if search_query:
            queryset = queryset.filter(name__icontains=search_query)

        if body_part_filter:
            queryset = queryset.filter(body_part__id=body_part_filter)

        if sort_by == 'name':
            queryset = queryset.order_by('name')
        elif sort_by == 'public':
            queryset = queryset.filter(public=True).order_by('name')
        elif sort_by == 'private':
            queryset = queryset.filter(public=False).order_by('name')
        else:
            queryset = queryset.order_by('name')

        return queryset.distinct()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ExercisesView, self).get_context_data(**kwargs)

        search_query, sort_by, body_part_filter = self.fetch_query_params()

        context['search'] = search_query
        context['sort_by'] = sort_by
        context['selected_body_part'] = body_part_filter
        context['body_parts'] = BodyPart.objects.all()

        context['training_plan'] = self.request.GET.get('training_plan', None)

        return context


class ExerciseDetailView(ExercisesOwnerRequiredMixin, DetailView):
    model = Exercise
    template_name = 'dashboard/exercise_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = AddExerciseToPlanForm()
        context['training_plan'] = self.request.GET.get('training_plan', None)

        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = AddExerciseToPlanForm(request.POST)
        training_plan_id = int(self.request.GET.get('training_plan', None))

        if form.is_valid():
            series = form.cleaned_data['series']
            reps = form.cleaned_data['reps']

            exercise_info = TrainingPlanExerciseInfo.objects.create(
                exercise=self.object,
                series=series,
                reps=reps
            )

            if training_plan_id:
                try:
                    training_plan = UserTrainingPlans.objects.get(id=training_plan_id)
                    max_order = training_plan.exercises_info.aggregate(models.Max('ordering'))['ordering__max'] or 0
                    exercise_info.ordering = max_order + 1
                    exercise_info.save()
                    training_plan.exercises_info.add(exercise_info)

                    return redirect(reverse_lazy('training_plan_detail', args=[training_plan.id]))

                except UserTrainingPlans.DoesNotExist:
                    form.add_error(None, "The training plan provided does not exist.")

        return self.render_to_response(self.get_context_data(form=form))


class ExerciseEditView(ExercisesOwnerRequiredMixin, UpdateView):
    model = Exercise
    form_class = ExerciseForm
    template_name = 'dashboard/exercise_edit.html'
    context_object_name = 'exercise'

    def get_success_url(self):
        return reverse_lazy('exercise_detail', kwargs={'pk': self.object.pk})

    def get_object(self, queryset=None):
        exercise = super().get_object(queryset)
        if not exercise.public and exercise.user != self.request.user:
            raise Http404("You do not have permission to edit this exercise.")
        return exercise

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['body_part'].help_text = None
        form.fields['name'].help_text = None
        return form


class CreateExerciseView(CreateView):
    model = Exercise
    form_class = CreateExerciseForm
    template_name = 'dashboard/exercise_create.html'
    success_url = reverse_lazy('exercises')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class DeleteExerciseView(ExercisesOwnerRequiredMixin, DeleteView):
    model = Exercise
    template_name = 'dashboard/exercise_delete.html'
    success_url = reverse_lazy('exercises')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionError("Yoy do not have permission to delete this exercise.")
        return obj