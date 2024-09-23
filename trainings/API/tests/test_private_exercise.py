from django.test import TestCase
from django.urls import reverse
import json
from rest_framework import status
from trainings.models import User, BodyPart, Exercise
from rest_framework_simplejwt.tokens import RefreshToken


class TestPrivateExerciseApi(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="tester", password='tester')
        self.token = RefreshToken.for_user(self.user)
        self.auth_header = {'AUTHORIZATION': f'Bearer {self.token.access_token}'}

        self.xyz = BodyPart.objects.create(name='Chest test')

        self.public_exercise = Exercise.objects.create(name='Public Chest Press', public=True)
        self.public_exercise.body_part.set([self.xyz])

        self.private_exercise = Exercise.objects.create(name='Private Chest Press', user=self.user)
        self.private_exercise.body_part.set([self.xyz])



    def test_CreatePrivateExercise_returns_201_when_provided_correct_params(self):
        data = {"name": "Bench Press", "body_part": [self.xyz.pk]}
        response = self.client.post(reverse('create-exercise'), data=data, headers=self.auth_header)

        response_data = json.loads(response.content)

        self.assertEqual(response_data['name'], 'Bench Press')
        self.assertEqual(response_data['public'], False)
        self.assertEqual(response_data['user'], self.user.pk)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_CreatePrivateExercise_returns_400_when_not_provided_required_params(self):
        data = {"body_part": [1]}
        response = self.client.post(reverse('create-exercise'), data=data, headers=self.auth_header)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data['name'], ['This field is required.'])

    def test_ReadPublicExercise(self):
        response = self.client.get(reverse('read-public-exercises'))
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data[0]["name"], 'Public Chest Press')

    def test_CreatePrivateExercise_returns_401_when_authorization_token_not_provided(self):
        data = {"name": "Triceps Extension", "body_part": [1]}
        response = self.client.post(reverse('create-exercise'), data=data)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_ReadPrivateExercise(self):
        response = self.client.get(reverse('read-private-exercises'), headers=self.auth_header)
        response_data = json.loads(response.content)
        self.assertEqual(self.user.pk, response_data[0]['user'])
    def test_UpdatePrivateExercise_returns_201_when_provided_correct_data(self):
        data = {'name': "Super Private Chest Press"}
        response = self.client.patch(reverse('update-private-exercise', kwargs={'pk': self.private_exercise.pk}), data=data,
                                     headers=self.auth_header, content_type='application/json')
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['name'], 'Super Private Chest Press')

    def test_UpdatePrivateExercise_returns_401_when_authorization_token_not_provided(self):
        data = {'name': "Super Private Chest Press"}
        response = self.client.patch(reverse('update-private-exercise', kwargs={'pk': 2}), data=data,
                                     content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_DeletePrivateExercise_returns_401_when_authorization_token_not_provided(self):
        response = self.client.delete(reverse('delete-exercise', kwargs={'pk': 2}),
                                      content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_DeletePrivateExercise_returns_204_when_authorization_token_provided(self):
        response = self.client.delete(reverse('delete-exercise', kwargs={'pk': self.private_exercise.pk}),
                                      content_type='application/json', headers=self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)