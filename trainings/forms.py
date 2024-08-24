from django import forms
from .models import Exercise

class CalculatorForm(forms.Form):
    female = forms.ChoiceField(
        choices=[(False, 'Male'), (True, 'Female')],
        label='Gender',
        widget=forms.Select(attrs={
            'class': 'form-control',
            'placeholder': 'Gender',
            'id': 'calculator-gender'
        })
    )
    body = forms.FloatField(
        max_value=1000,
        label='Body Weight(in kg)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Body weight',
            'id': 'calculator-weight'
        })
    )
    sq = forms.FloatField(
        max_value=1000,
        label='Squat Weight(in kg)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Squat Weight',
            'id': 'calculator-squat'
        })
    )
    sq_reps = forms.IntegerField(
        max_value=100,
        label='Squat Reps',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Squat Reps',
            'id': 'calculator-squat-reps'
        })
    )
    bp = forms.FloatField(
        max_value=1000,
        label='Bench Press Weight(in kg)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Bench Press Weight',
            'id': 'calculator-bench'
        })
    )
    bp_reps = forms.IntegerField(
        max_value=100,
        label='Bench Press Reps',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Bench Reps',
        })
    )
    dl = forms.FloatField(
        max_value=1000,
        label='Deadlift Weight(in kg)',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Deadlift Weight',
            'id': 'calculator-deadlift'
        })
    )
    dl_reps = forms.IntegerField(
        max_value=100,
        label='Deadlift Reps',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Deadlift Reps',
            'id': 'calculator-deadlift-reps'
        })
    )

    def clean_gender(self):
        gender = self.cleaned_data['gender']

        return False if gender == 'male' else True


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'body_part']
