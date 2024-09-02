from django import forms
from .models import Exercise, UserTrainingPlans, BodyPart



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


class CreateExerciseForm(forms.ModelForm):
    name = forms.CharField(
        help_text="",
        required=True
    )
    body_part = forms.ModelMultipleChoiceField(
        queryset=BodyPart.objects.all().order_by('name'),
        widget=forms.SelectMultiple(attrs={
            'size': '14',
            'style': 'height: auto',
        }),
        help_text=''
    )
    class Meta:
        model = Exercise
        fields = ['name', 'body_part']


    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        exercise = super().save(commit=False)
        if self.user:
            exercise.user = self.user
        if commit:
            exercise.save()

        return exercise


class CreateTrainingPlanForm(forms.ModelForm):
    name = forms.CharField(
        help_text=""
    )

    class Meta:
        model = UserTrainingPlans
        fields = ['name']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        training_plan = super().save(commit=False)
        if self.user:
            training_plan.user = self.user
        if commit:
            training_plan.save()

        return training_plan


class UpdateTrainingPlanForm(forms.ModelForm):
    name = forms.CharField(
        help_text=""
    )

    class Meta:
        model = UserTrainingPlans
        fields = ['name']
