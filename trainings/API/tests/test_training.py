from django.test import TestCase
from django.urls import reverse
import json
from rest_framework import status
from trainings.models import User, UserTrainingPlans, Training
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import datetime


class TestTraining(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="tester", password='tester')
        self.token = RefreshToken.for_user(self.user)
        self.auth_header = {'AUTHORIZATION': f'Bearer {self.token.access_token}'}

        self.trainingplan = UserTrainingPlans.objects.create(name='Test Plan', user=self.user)

        self.training = Training.objects.create(
            user_id=self.user.pk,
            training_plan=self.trainingplan,
            start_time=timezone.make_aware(datetime(2024, 1, 1)),
            end_time=timezone.make_aware(datetime(2024, 1, 1)),
            training_duration='100:0:0'
        )

    def test_CreateTraining_returns_201_when_provided_correct_data(self):
        data = {'start_time': '2024-01-01', 'end_time': '2024-01-01', 'training_duration': 100, 'training_plan': self.trainingplan.pk}
        response = self.client.post(reverse('create-training'), data=data, content_type='application/json',
                                    headers=self.auth_header)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['user'], self.user.pk)

    def test_CreateTraining_returns_400_when_not_provided_correct_data(self):
        data = {}
        response = self.client.post(reverse('create-training'), data=data, content_type='application/json',
                                    headers=self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_CreateTraining_returns_401_when_authorization_token_not_provided(self):
        data = {}
        response = self.client.post(reverse('create-training'), data=data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ReadTrainings_returns_200_when_provided_correct_data(self):
        response = self.client.get(reverse('read-trainings'), headers=self.auth_header)
        response_data = json.loads(response.content)

        self.assertEqual(response_data[0]['user'], self.user.pk)
        self.assertEqual(response_data[0]['training_plan'], self.trainingplan.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ReadTrainings_returns_401_when_not_provided_authorization_token(self):
        response = self.client.get(reverse('read-trainings'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_UpdateTraining_returns_201_when_provided_correct_data(self):
        data = {'note': 'ads'}
        response = self.client.patch(reverse('update-training', kwargs={'pk': self.training.pk}), data=data,
                                     headers=self.auth_header, content_type='application/json')
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['note'], 'ads')

    def test_UpdateTraining_returns_401_when_authorization_token_not_provided(self):
        data = {'user': "2"}
        response = self.client.patch(reverse('update-training', kwargs={'pk': 1}), data=data,
                                     content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_DeleteTraining_returns_401_when_authorization_token_not_provided(self):
        response = self.client.delete(reverse('delete-training', kwargs={'pk': 1}),
                                      content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_DeleteTraining_returns_204_when_authorization_token_provided(self):
        response = self.client.delete(reverse('delete-training', kwargs={'pk': self.training.pk}),
                                      content_type='application/json',  headers=self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)