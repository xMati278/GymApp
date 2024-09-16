from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from trainings.models import Exercise, UserTrainingPlans, TrainingExercise, Training, TrainingPlanExerciseInfo
from trainings.forms import CreateTrainingPlanForm, UpdateTrainingPlanForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from dashboard.mixins import TrainingPlanOwnerRequiredMixin
import json


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


class TrainingPlanDetailView(TrainingPlanOwnerRequiredMixin, DetailView):
    model = UserTrainingPlans
    template_name = 'dashboard/training_plan_detail.html'
    context_object_name = 'training_plan'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        training_plan = self.get_object()

        context['last_training'] = training_plan.last_training
        context['exercises_info'] = training_plan.exercises_info.all().order_by('ordering')
        return context


class TrainingPlanEditView(TrainingPlanOwnerRequiredMixin, UpdateView):
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


class DeleteTrainingPlanView(TrainingPlanOwnerRequiredMixin, DeleteView):
    model = UserTrainingPlans
    template_name = 'dashboard/confirm_delete_training_plan.html'
    context_object_name = 'training_plan'
    success_url = reverse_lazy('training_plans')


class ActiveTrainingPlanView(TrainingPlanOwnerRequiredMixin, DetailView):
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
    data = json.loads(request.body)
    exercise_id = data.get('exercise_id')
    reps = data.get('reps')
    weight = data.get('weight')
    training_id = data.get('training_id')

    try:
        exercise = get_object_or_404(Exercise, id=exercise_id)
        training = get_object_or_404(Training, id=training_id)

        TrainingExercise.objects.create(
            training=training,
            exercise=exercise,
            series=1,
            reps=reps,
            weight=weight
        )

        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

class DeleteExerciseFromPlanView(DeleteView):
    model = TrainingPlanExerciseInfo
    template_name = 'dashboard/confirm_delete_training_plan_exercise.html'

    def get_success_url(self):
        training_plan = self.object.training_plans.first()
        return reverse_lazy('training_plan_detail', kwargs={'pk': training_plan.pk})
