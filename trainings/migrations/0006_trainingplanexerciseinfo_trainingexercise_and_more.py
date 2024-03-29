# Generated by Django 4.2.7 on 2024-01-04 19:49

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0005_remove_exercise_body_part_exercise_body_part'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingPlanExerciseInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.PositiveIntegerField(help_text='series number', validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('reps', models.PositiveIntegerField(help_text='reps amount', validators=[django.core.validators.MinValueValidator(1)])),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercise_id', to='trainings.exercise')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('series', models.PositiveIntegerField(help_text='series number', validators=[django.core.validators.MaxValueValidator(100), django.core.validators.MinValueValidator(1)])),
                ('reps', models.PositiveIntegerField(help_text='reps amount', validators=[django.core.validators.MinValueValidator(1)])),
                ('weight', models.FloatField(help_text='weight amount', validators=[django.core.validators.MinValueValidator(1)])),
                ('training', models.ForeignKey(help_text='exercise from this training', on_delete=django.db.models.deletion.CASCADE, related_name='training_id', to='trainings.training')),
            ],
        ),
        migrations.AddField(
            model_name='usertrainingplans',
            name='exercises_info',
            field=models.ManyToManyField(to='trainings.trainingplanexerciseinfo'),
        ),
    ]
