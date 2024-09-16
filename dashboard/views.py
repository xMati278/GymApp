from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from accounts.forms import LoginForm, RegisterForm
from trainings.forms import CalculatorForm
from trainings.calculators import Calculators
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView, DeleteView
from trainings.models import Exercise, BodyPart, UserTrainingPlans, TrainingPlanExerciseInfo, TrainingExercise, Training
from .const import CALCULATOR_KEY_TO_DISPLAY_MAP
from django.http import Http404
from trainings.forms import (ExerciseForm, CreateExerciseForm, CreateTrainingPlanForm, UpdateTrainingPlanForm,
                             AddExerciseToPlanForm)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

class LoginView(FormView):
    template_name = 'dashboard/login.html'
    form_class = LoginForm
    success_url = reverse_lazy('training_plans')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(self.request, username=username, password=password)
        if user:
            login(self.request, user)
            return super().form_valid(form)
        else:
            form.add_error(None, 'Incorrect Username or Password')
            return self.form_invalid(form)


class RegisterView(FormView):
    template_name = 'dashboard/register.html'
    form_class = RegisterForm
    success_url = reverse_lazy('training_plans')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']

        if User.objects.filter(username=username).exists():
            form.add_error(None, 'Username already taken')
            return self.form_invalid(form)
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            login(self.request, user)
            return super().form_valid(form)


class CalculatorView(FormView):
    template_name = 'dashboard/calculator.html'
    form_class = CalculatorForm
    success_url = reverse_lazy('calculator_result')

    def form_valid(self, form):
        data = {}
        for key, value in form.cleaned_data.items():
            data[key] = value

        calculator_result = Calculators.total_logic(**data)
        calculator_result = self.convert_result_keys(data=calculator_result)
        self.request.session['calculator_result'] = calculator_result

        return redirect('calculator_result')

    @staticmethod
    def convert_result_keys(data):
        converted_data = {}

        for key, value in data.items():
            new_key = CALCULATOR_KEY_TO_DISPLAY_MAP.get(key, key)
            converted_data[new_key] = value

        return converted_data


class CalculatorResultView(TemplateView):
    template_name = 'dashboard/calculator_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calculator_result'] = self.request.session.get('calculator_result', None)
        return context


class CreateTrainingPlans(CreateView):
    model = Exercise
    form_class = CreateTrainingPlanForm
    template_name = 'dashboard/training_plan_create.html'
    success_url = reverse_lazy('training_plans')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class ReadTrainingPlans(LoginRequiredMixin, ListView):
    template_name = 'dashboard/training_plans.html'
    paginate_by = 10
    model = UserTrainingPlans

    def get_queryset(self):
        user = self.request.user
        return UserTrainingPlans.objects.filter(user=user)


class TrainingPlanDetailView(UserPassesTestMixin, DetailView):
    model = UserTrainingPlans
    template_name = 'dashboard/training_plan_detail.html'
    context_object_name = 'training_plan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        training_plan = self.get_object()

        context['last_training'] = training_plan.last_training
        context['exercises_info'] = training_plan.exercises_info.all().order_by('ordering')
        return context

    def test_func(self):
        training_plan = self.get_object()

        return self.request.user == training_plan.user

    def handle_no_permission(self):
        return redirect(reverse_lazy('training_plans'))

class TrainingPlanEditView(UpdateView):
    model = UserTrainingPlans
    form_class = UpdateTrainingPlanForm
    template_name = 'dashboard/training_plan_edit.html'
    context_object_name = 'training_plan'

    def get_success_url(self):
        return reverse_lazy('training_plan_detail', kwargs={'pk': self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['exercises_info'] = self.object.exercises_info.all().order_by('ordering')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        training_plan = self.object

        for exercise_info in training_plan.exercises_info.all():
            new_ordering = request.POST.get(f'order-{exercise_info.id}', exercise_info.ordering)
            new_series = request.POST.get(f'series-{exercise_info.id}', exercise_info.series)
            new_reps = request.POST.get(f'reps-{exercise_info.id}', exercise_info.reps)

            exercise_info.ordering = int(new_ordering)
            exercise_info.series = int(new_series)
            exercise_info.reps = int(new_reps)
            exercise_info.save()

        if request.headers.get('HX-Request'):
            context = self.get_context_data()
            return render(request, 'dashboard/partials/training_plan_exercises_list.html', context)

        return redirect(self.get_success_url())


class DeleteTrainingPlanView(DeleteView):
    model = UserTrainingPlans
    template_name = 'dashboard/confirm_delete_training_plan.html'
    context_object_name = 'training_plan'
    success_url = reverse_lazy('training_plans')


class ActiveTrainingPlanView(DetailView):
    model = UserTrainingPlans
    template_name = 'dashboard/training_plan_active.html'
    context_object_name = 'training_plan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        training_plan = self.get_object()
        current_training = get_object_or_404(Training, id=2)

        context['last_training'] = training_plan.last_training
        context['exercises_info'] = training_plan.exercises_info.all()
        context['current_training'] = current_training
        return context


@csrf_exempt
@require_POST
def add_training_exercise(request):
    import json
    data = json.loads(request.body)
    exercise_id = data.get('exercise_id')
    reps = data.get('reps')
    weight = data.get('weight')
    training_id = data.get('training_id')

    try:
        exercise = get_object_or_404(Exercise, id=exercise_id)
        training = get_object_or_404(Training, id=training_id)  # Use the correct Training instance

        TrainingExercise.objects.create(
            training=training,
            exercise=exercise,
            series=1,  # Adjust or set default as needed
            reps=reps,
            weight=weight
        )

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

def history_view(request): #TODO do zrobienia
    return render(request, 'dashboard/history.html')


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


class ExerciseDetailView(DetailView):
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


class ExerciseEditView(UpdateView):
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


class DeleteExerciseView(DeleteView):
    model = Exercise
    template_name = 'dashboard/exercise_delete.html'
    success_url = reverse_lazy('exercises')

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj.user != self.request.user:
            raise PermissionError("Yoy do not have permission to delete this exercise.")
        return obj


class DeleteExerciseFromPlanView(DeleteView):
    model = TrainingPlanExerciseInfo
    template_name = 'dashboard/confirm_delete_training_plan_exercise.html'

    def get_success_url(self):
        training_plan = self.object.training_plans.first()
        return reverse_lazy('training_plan_detail', kwargs={'pk': training_plan.pk})


def records_view(request): #TODO do zrobienia
    return render(request, 'dashboard/records.html')
