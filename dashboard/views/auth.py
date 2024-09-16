from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from accounts.forms import LoginForm, RegisterForm
from django.views.generic import FormView
from django.urls import reverse_lazy


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
