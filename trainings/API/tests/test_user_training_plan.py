from django.test import TestCase
from django.urls import reverse
import json
from rest_framework import status
from trainings.models import User, UserTrainingPlans
from rest_framework_simplejwt.tokens import RefreshToken


class TestUserTrainingPlanApi(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="tester", password='tester') # nosec B106
        self.token = RefreshToken.for_user(self.user)
        self.auth_header = {'AUTHORIZATION': f'Bearer {self.token.access_token}'}

        self.trainingplan = UserTrainingPlans.objects.create(name='Test Plan', user=self.user)

    def test_CreateUserTrainingPlan_returns_201_when_provided_correct_data(self):
        data = {'name': 'Extra GPP'}
        response = self.client.post(reverse('create-user-training-plan'), data=data, content_type='application/json',
                                    headers=self.auth_header)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['name'], 'Extra GPP')

    def test_CreateUserTrainingPlan_returns_400_when_not_provided_correct_data(self):
        data = {}
        response = self.client.post(reverse('create-user-training-plan'), data=data, content_type='application/json',
                                    headers=self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_CreateUserTrainingPlan_returns_401_when_authorization_token_not_provided(self):
        data = {'name': 'Extra GPP'}
        response = self.client.post(reverse('create-user-training-plan'), data=data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ReadUserTrainingPlans_returns_200_when_provided_correct_data(self):
        response = self.client.get(reverse('read-user-training-plans'), headers=self.auth_header)
        response_data = json.loads(response.content)

        self.assertEqual(response_data[0]['name'], 'Test Plan')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ReadUserTrainingPlans_returns_401_when_not_provided_authorization_token(self):
        response = self.client.get(reverse('read-user-training-plans'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_UpdateUserTrainingPlans_returns_200_when_provided_correct_data(self):
        data = {'name': "Push Test"}
        response = self.client.patch(reverse('update-user-training-plan', kwargs={'pk': self.trainingplan.pk}), data=data,
                                     headers=self.auth_header, content_type='application/json')
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['name'], 'Push Test')

    def test_UpdateUserTrainingPlans_returns_401_when_authorization_token_not_provided(self):
        data = {'name': "Push Test"}
        response = self.client.patch(reverse('update-user-training-plan', kwargs={'pk': 1}), data=data,
                                     content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_DeleteUserTrainingPlan_returns_401_when_authorization_token_not_provided(self):
        response = self.client.delete(reverse('delete-user-training-plan', kwargs={'pk': 1}),
                                      content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_DeleteUserTrainingPlan_returns_204_when_authorization_token_provided(self):
        response = self.client.delete(reverse('delete-user-training-plan', kwargs={'pk': self.trainingplan.pk}),
                                      content_type='application/json', headers=self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
