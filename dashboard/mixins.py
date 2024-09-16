from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy


class TrainingPlanOwnerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        training_plan = self.get_object()

        return self.request.user == training_plan.user

    def handle_no_permission(self):
        return redirect(reverse_lazy('training_plans'))