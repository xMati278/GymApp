from django.test import TestCase
from django.urls import reverse
import json
from rest_framework import status
from trainings.models import User, Exercise, Category, TrainingRecord
from rest_framework_simplejwt.tokens import RefreshToken


class TestTrainingRecordApi(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="tester", password='tester') # nosec B106
        self.token = RefreshToken.for_user(self.user)
        self.auth_header = {'AUTHORIZATION': f'Bearer {self.token.access_token}'}

        self.onerm_category = Category.objects.create(category='One rep max.')

        self.public_exercise = Exercise.objects.create(name='Public Chest Press', public=True)
        self.private_exercise = Exercise.objects.create(name='Private Chest Press', user=self.user)

        self.user_record = TrainingRecord.objects.create(
            user=self.user,
            exercise=self.private_exercise,
            category=self.onerm_category,
            value=100
        )

    def test_CreateTrainingRecord_returns_201_when_provided_correct_data(self):
        data = {'user': self.user.pk, 'exercise': self.public_exercise.pk, 'category': self.onerm_category.pk, 'value': 100}
        response = self.client.post(reverse('create-training-record'), data=data, content_type='application/json',
                                    headers=self.auth_header)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['user'], self.user.pk)

    def test_CreateTrainingRecord_returns_400_when_not_provided_correct_data(self):
        data = {}
        response = self.client.post(reverse('create-training-record'), data=data, content_type='application/json',
                                    headers=self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_CreateTrainingRecord_returns_401_when_authorization_token_not_provided(self):
        data = {}
        response = self.client.post(reverse('create-training-record'), data=data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ReadTrainingsRecord_returns_200_when_provided_correct_data(self):
        response = self.client.get(reverse('read-training-record'), headers=self.auth_header)
        response_data = json.loads(response.content)

        self.assertEqual(response_data[0]['user'], self.user.pk)
        self.assertEqual(response_data[0]['category'], self.onerm_category.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ReadTrainingsRecord_returns_401_when_not_provided_authorization_token(self):
        response = self.client.get(reverse('read-training-record'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_UpdateTrainingRecord_returns_201_when_provided_correct_data(self):
        data = {'value': 150}
        response = self.client.patch(reverse('update-training-record', kwargs={'pk': self.user_record.pk}), data=data,
                                     headers=self.auth_header, content_type='application/json')
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['value'], 150)

    def test_UpdateTrainingRecord_returns_401_when_authorization_token_not_provided(self):
        data = {'value': 150}
        response = self.client.patch(reverse('update-training-record', kwargs={'pk': self.user_record.pk}), data=data,
                                     content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_DeleteTrainingRecord_returns_401_when_authorization_token_not_provided(self):
        response = self.client.delete(reverse('delete-training-record', kwargs={'pk': self.user_record.pk}),
                                      content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_DeleteTrainingRecord_returns_204_when_authorization_token_provided(self):
        response = self.client.delete(reverse('delete-training-record', kwargs={'pk': self.user_record.pk}),
                                      content_type='application/json',  headers=self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)