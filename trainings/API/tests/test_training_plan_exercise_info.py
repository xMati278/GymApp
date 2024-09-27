from django.test import TestCase
from django.urls import reverse
import json
from rest_framework import status
from trainings.models import User, Exercise, TrainingPlanExerciseInfo
from rest_framework_simplejwt.tokens import RefreshToken


class TestTrainingPlanExerciseInfoApi(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user(username="tester", password='tester')  # nosec B106
        self.token = RefreshToken.for_user(self.user)
        self.auth_header = {'AUTHORIZATION': f'Bearer {self.token.access_token}'}

        self.public_exercise = Exercise.objects.create(name='Public Chest Press', public=True)

        self.exercise_info = TrainingPlanExerciseInfo.objects.create(
            exercise=self.public_exercise,
            series=3,
            reps=3
        )


    def test_CreateTrainingPlanExerciseInfo_returns_201_when_provided_correct_data(self):
        data = {'exercise': self.public_exercise.pk, 'series': 2, 'reps': 5}
        response = self.client.post(reverse('api-training-plan-exercise-info'), data=data, content_type='application/json',
                                    headers=self.auth_header)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['series'], 2)

    def test_CreateTrainingPlanExerciseInfo_returns_400_when_not_provided_correct_data(self):
        data = {}
        response = self.client.post(reverse('api-training-plan-exercise-info'), data=data, content_type='application/json',
                                    headers=self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_CreateTrainingPlanExerciseInfo_returns_401_when_authorization_token_not_provided(self):
        data = {}
        response = self.client.post(reverse('api-training-plan-exercise-info'), data=data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ReadTrainingPlanExerciseInfo_returns_200_when_provided_correct_data(self):
        response = self.client.get(reverse('api-training-plan-exercise-info'), headers=self.auth_header)
        response_data = json.loads(response.content)
        self.assertEqual(response_data[0]['reps'], 3)
        self.assertEqual(response_data[0]['exercise'], self.public_exercise.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ReadTrainingPlanExerciseInfo_returns_401_when_not_provided_authorization_token(self):
        response = self.client.get(reverse('api-training-plan-exercise-info'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_UpdateTrainingPlanExerciseInfo_returns_201_when_provided_correct_data(self):
        data = {'reps': 5}
        response = self.client.patch(reverse('api-edit-training-plan-exercise-info', kwargs={'pk': self.exercise_info.pk}), data=data,
                                     headers=self.auth_header, content_type='application/json')
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['reps'], 5)

    def test_UpdateTrainingPlanExerciseInfo_returns_401_when_authorization_token_not_provided(self):
        data = {'reps': 5}
        response = self.client.patch(reverse('api-edit-training-plan-exercise-info', kwargs={'pk': self.exercise_info.pk}), data=data,
                                     content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_DestroyTrainingPlanExerciseInfo_returns_401_when_authorization_token_not_provided(self):
        response = self.client.delete(reverse('api-edit-training-plan-exercise-info', kwargs={'pk': self.exercise_info.pk}),
                                      content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_DestroyTrainingPlanExerciseInfo_returns_204_when_authorization_token_provided(self):
        response = self.client.delete(reverse('api-edit-training-plan-exercise-info', kwargs={'pk': self.exercise_info.pk}),
                                      content_type='application/json',  headers=self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)