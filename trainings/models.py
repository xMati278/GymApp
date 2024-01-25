from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

class BodyPart(models.Model):
    name = models.CharField(max_length=30, help_text='name of the body part')

    def __str__(self):
        return f'{self.pk}. {self.name}'


class Exercise(models.Model):
    name = models.CharField(max_length=100, help_text='name of exercise')
    body_part = models.ManyToManyField(BodyPart, help_text='body part for exercise')
    public = models.BooleanField(default=False, help_text='defines if exercise is visible for other users')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, default=None,
                             related_name='exercises', help_text='exercise owner')

    def __str__(self):
        return f'{self.pk}. {self.name} {("private: ",(self.user.username)) if self.public is False else "public" }'

class TrainingPlanExerciseInfo(models.Model):
    exercise = models.ForeignKey(Exercise,null=True, on_delete=models.CASCADE, related_name='exercise_id')
    series = models.PositiveIntegerField(help_text="series number", validators=[MaxValueValidator(100),
                                                                                MinValueValidator(1)])
    reps = models.PositiveIntegerField(help_text="reps amount", validators=[MinValueValidator(1)])

class UserTrainingPlans(models.Model): # TrainingPlan
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_training_plans', help_text='training plan owner')
    name = models.CharField(max_length=100, help_text='training plan name')
    last_training = models.DateTimeField(blank=True, null=True, help_text='date of last training')
    exercises = models.ManyToManyField(Exercise, blank=True,default=None, help_text='exercises assigned to this plan')
    exercises_info = models.ManyToManyField(TrainingPlanExerciseInfo, blank=True) # [exercise: 1, resp:5, series: 5]

    def __str__(self) -> str:
        return f'{self.pk}. {self.user.username} - {self.name}'


class Training(models.Model):
    start_time = models.DateTimeField(blank=False, null=False, help_text='training start time')
    end_time = models.DateTimeField(blank=False, null=False, help_text='training end time')
    training_duration = models.DurationField(blank=False, null=False, help_text='training duration')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='trainings', help_text='training owner')
    training_plan = models.ForeignKey(UserTrainingPlans, on_delete=models.CASCADE, related_name='trainings', help_text='training plan')
    note = models.TextField(null=True, blank=True, default=None, help_text='optional training note')

    def __str__(self) -> str:
        return f'{self.user.username} - {self.training_plan.name} time: {self.training_duration}'


class Category(models.Model):
    category = models.CharField(max_length=50, help_text='training record category')

    def __str__(self) -> str:
        return self.category


class TrainingRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='training_records', help_text='record owner')
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, related_name='training_records', help_text='record exercise')
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                 related_name='training_records', help_text='record category')
    value = models.FloatField(default=0, help_text='value of the record')

    def __str__(self) -> str:
        return f'{self.user.username} - {self.exercise.name} - {self.category.category}: {self.value}'


class TrainingExercise(models.Model):
    training = models.ForeignKey(Training, on_delete=models.CASCADE, related_name='training_id',
                                 help_text="exercise from this training")
    exercise = models.ForeignKey(Exercise,default=None, on_delete=models.CASCADE, related_name='training_exercise',
                                 help_text='record exercise')
    series = models.PositiveIntegerField(help_text="series number", validators=[MaxValueValidator(100),
                                                                                MinValueValidator(1)])
    reps = models.PositiveIntegerField(help_text="reps amount", validators=[MinValueValidator(1)])
    weight = models.FloatField(help_text="weight amount", validators=[MinValueValidator(1)])

    def __str__(self) -> str:
        return f'{self.training.user}, training: {self.training.id}, series: {self.series}, reps: {self.reps},' \
               f' weight: {self.weight}'



