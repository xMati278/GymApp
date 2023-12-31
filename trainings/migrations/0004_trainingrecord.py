# Generated by Django 4.2.7 on 2023-12-07 20:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trainings', '0003_category_training'),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField(default=0, help_text='value of the record')),
                ('category', models.ForeignKey(help_text='record category', on_delete=django.db.models.deletion.CASCADE, related_name='training_records', to='trainings.category')),
                ('exercise', models.ForeignKey(help_text='record exercise', on_delete=django.db.models.deletion.CASCADE, related_name='training_records', to='trainings.exercise')),
                ('user', models.ForeignKey(help_text='record owner', on_delete=django.db.models.deletion.CASCADE, related_name='training_records', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
