from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from accounts.forms import LoginForm, RegisterForm
from trainings.forms import CalculatorForm
from trainings.calculators import Calculators
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from trainings.models import Exercise, BodyPart
from .const import CALCULATOR_KEY_TO_DISPLAY_MAP
from django.http import Http404
from trainings.forms import ExerciseForm


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


def training_plans_view(request): #TODO do zrobienia
    return render(request, 'dashboard/training_plans.html')


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
            queryset = queryset.filter(public=True)
        elif sort_by == 'private':
            queryset = queryset.filter(public=False)

        return queryset.distinct()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ExercisesView, self).get_context_data(**kwargs)

        search_query, sort_by, body_part_filter = self.fetch_query_params()

        context['search'] = search_query
        context['sort_by'] = sort_by
        context['selected_body_part'] = body_part_filter
        context['body_parts'] = BodyPart.objects.all()

        return context


class ExerciseDetailView(DetailView):
    model = Exercise
    template_name = 'dashboard/exercise_detail.html'


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

def records_view(request): #TODO do zrobienia
    return render(request, 'dashboard/records.html')
