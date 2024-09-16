from django.shortcuts import redirect
from trainings.forms import CalculatorForm
from trainings.calculators import Calculators
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from dashboard import const


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
            new_key = const.CALCULATOR_KEY_TO_DISPLAY_MAP.get(key, key)
            converted_data[new_key] = value

        return converted_data


class CalculatorResultView(TemplateView):
    template_name = 'dashboard/calculator_result.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['calculator_result'] = self.request.session.get('calculator_result', None)
        return context
