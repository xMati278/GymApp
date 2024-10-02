from django.test import TestCase
from django.urls import reverse
import json
from rest_framework import status
from trainings.models import User, BodyPart, Exercise, UserTrainingPlans, Training, TrainingExercise
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import datetime


class TestTrainingExerciseApi(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="tester", password='tester')  # nosec B106
        self.token = RefreshToken.for_user(self.user)
        self.auth_header = {'AUTHORIZATION': f'Bearer {self.token.access_token}'}

        self.exercise = Exercise.objects.create(name='Chest Press', public=True)
        self.trainingplan = UserTrainingPlans.objects.create(name='Test Plan', user=self.user)

        self.training = Training.objects.create(
            user=self.user,
            training_plan=self.trainingplan,
            start_time=timezone.make_aware(datetime(2024, 1, 1)),
            end_time=timezone.make_aware(datetime(2024, 1, 1)),
            training_duration='100:0:0'
        )

        self.training_exercise = TrainingExercise.objects.create(
            training=self.training,
            exercise=self.exercise,
            series=3,
            reps=5,
            weight=100
        )

    @classmethod
    def setUpTestData(cls):
        BodyPart.objects.create(name='Triceps')
        BodyPart.objects.create(name='Biceps')

    def test_CreateTrainingExercise_returns_201_when_provided_correct_data(self):
        data = {"series": 3, "reps": 5, "weight": 50, "training": self.training.pk, 'exercise': self.exercise.pk}
        response = self.client.post(reverse('api-training-exercises-list'), data=data, content_type='application/json',
                                    headers=self.auth_header)
        response_data = json.loads(response.content)
        obj = TrainingExercise.objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['id'], obj.id)
        self.assertEqual(response_data['series'], 3)
        self.assertEqual(response_data['reps'], 5)
        self.assertEqual(response_data['weight'], 50)
        self.assertEqual(response_data['training'], self.training.pk)
        self.assertEqual(response_data['exercise'], self.exercise.pk)

    def test_CreateTrainingExercise_returns_400_when_not_provided_correct_data(self):
        data = {}
        response = self.client.post(reverse('api-training-exercises-list'), data=data, content_type='application/json',
                                    headers=self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_CreateTrainingExercise_returns_401_when_authorization_token_not_provided(self):
        data = {}
        response = self.client.post(reverse('api-training-exercises-list'), data=data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ReadTrainingExercise_returns_200_when_provided_correct_data(self):
        response = self.client.get(reverse('api-training-exercises-list'), headers=self.auth_header)
        response_data = json.loads(response.content)

        self.assertEqual(response_data[0]['training'], self.training.pk)
        self.assertEqual(response_data[0]['reps'], 5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ReadTrainingExercise_returns_401_when_not_provided_authorization_token(self):
        response = self.client.get(reverse('api-training-exercises-list'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_UpdateTrainingExercise_returns_201_when_provided_correct_data(self):
        data = {'series': 1}
        response = self.client.patch(reverse('api-training-exercises-detail', kwargs={'pk': self.training_exercise.pk}), data=data,
                                     headers=self.auth_header, content_type='application/json')
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['series'], 1)

    def test_UpdateTrainingExercise_returns_401_when_authorization_token_not_provided(self):
        data = {'series': 1}
        response = self.client.patch(reverse('api-training-exercises-detail', kwargs={'pk': self.training_exercise.pk}), data=data,
                                     content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_DeleteTrainingExercise_returns_401_when_authorization_token_not_provided(self):
        response = self.client.delete(reverse('api-training-exercises-detail', kwargs={'pk': self.training_exercise.pk}),
                                      content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_DeleteTrainingExercise_returns_204_when_authorization_token_provided(self):
        response = self.client.delete(reverse('api-training-exercises-detail', kwargs={'pk': self.training_exercise.pk}),
                                      content_type='application/json', headers=self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
