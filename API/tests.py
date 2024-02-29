from django.test import TestCase
from django.urls import reverse
import json
from .calculators import Calculators
from rest_framework import status
from trainings.models import User, BodyPart, Exercise, UserTrainingPlans, Training, Category, TrainingRecord,\
    TrainingPlanExerciseInfo, TrainingExercise
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import datetime
# Create your tests here.


class TestApi(TestCase):
    def setUp(self) -> None:
        self.xyz = BodyPart.objects.create(name='Chest test')
        self.user = User.objects.create_user(username="tester", password='tester')# nosec B106
        self.user2 = User.objects.create_user(username="admin", password='admin')# nosec B106
        self.token = RefreshToken.for_user(self.user)
        self.auth_header = {'AUTHORIZATION': f'Bearer {self.token.access_token}'}
        # self.client.credentials = {'HTTP_AUTHORIZATION': f'Bearer {self.token}'}
        self.onerm_category = Category.objects.create(category='One rep max.')
        self.public_exercise = Exercise.objects.create(name='Public Chest Press', public=True)
        self.public_exercise.body_part.set([self.xyz])
        self.private_exercise = Exercise.objects.create(name='Private Chest Press', user=self.user)
        self.private_exercise.body_part.set([self.xyz])
        self.trainingplan = UserTrainingPlans.objects.create(name='Test Plan', user=self.user)
        self.trainingplan.exercises.set([self.public_exercise])
        self.training = Training.objects.create(user_id=self.user.pk, training_plan=self.trainingplan,
                                                start_time=timezone.make_aware(datetime(2024, 1, 1)),
                                                end_time=timezone.make_aware(datetime(2024, 1, 1)),
                                                training_duration='100:0:0')
        self.user_record = TrainingRecord.objects.create(user=self.user, exercise=self.private_exercise,
                                          category=self.onerm_category, value=100)
        self.exercise_info = TrainingPlanExerciseInfo.objects.create(exercise=self.public_exercise, series=3, reps=3)
        self.training_exercise = TrainingExercise.objects.create(training=self.training, exercise=self.private_exercise,
                                                                 series=3, reps=5, weight=100)

    @classmethod
    def setUpTestData(cls):
        BodyPart.objects.create(name='Triceps')
        BodyPart.objects.create(name='Biceps')

    def test_calculate_1rm_logic_returns_valid_data_when_provided_valid_data(self):
        few_reps_response = Calculators.calculate_1rm_logic(lift=100, reps=5)['result']
        one_rep_response = Calculators.calculate_1rm_logic(lift=100, reps=1)['result']

        self.assertEqual(few_reps_response, 115)
        self.assertEqual(one_rep_response, 100)

    def test_calculate_1rm_returns_400_when_provided_invalid_params_types(self):
        response = self.client.get(reverse('calculate-1rm'), {'reps': 'asd', 'lift': 'test'})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data['reps'][0], 'A valid integer is required.')
        self.assertEqual(response_data['lift'][0], 'A valid number is required.')

    def test_calculate_1rm_returns_error_when_not_provided_required_params(self):
        response = self.client.get(reverse('calculate-1rm'), {'reps': '5'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data['lift'][0], 'This field is required.')

    def test_calculate_1rm_returns_200_when_provided_valid_data(self):
        response = self.client.get(reverse('calculate-1rm'), {'reps': '1', 'lift': '120'})
        response_data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['result'], 120)

    def test_calculate_wilks_logic_returns_valid_data_when_provided_valid_data(self):
        response = Calculators.calculate_wilks_logic(female=True, body=80, lift=120)

        self.assertEqual(response['result'], 135.81)
        self.assertEqual(type(response['result']), float)

    def test_calculate_wilks_returns_400_when_provided_invalid_params_types(self):
        response = self.client.get(reverse('calculate-wilks'), {'female': 'whynot', 'body': 'maybe', 'lift': 'never'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data['female'][0], "Must be a valid boolean.")
        self.assertEqual(response_data['body'][0], "A valid number is required.")
        self.assertEqual(response_data['lift'][0], "A valid number is required.")

    def test_calculate_wilks_returns_error_when_not_provided_required_params(self):
        response = self.client.get(reverse('calculate-wilks'), {'female': 'True', 'lift': '100'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data['body'][0], 'This field is required.')

    def test_calculate_wilks_returns_200_when_provided_valid_data(self):
        response = self.client.get(reverse('calculate-wilks'), {'female': 'True', 'lift': 120, 'body': '80'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['result'], 135.81)

    def test_calculate_dots_logic_returns_valid_data_when_provided_valid_data(self):
        response = Calculators.calculate_dots_logic(female=True, body=80, lift=120)

        self.assertEqual(response['result'], 113.07)
        self.assertEqual(type(response['result']), float)

    def test_calculate_dots_returns_400_when_provided_invalid_params_types(self):
        response = self.client.get(reverse('calculate-dots'), {'female': 'whynot', 'body': 'maybe', 'lift': 'never'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data['female'][0], "Must be a valid boolean.")
        self.assertEqual(response_data['body'][0], "A valid number is required.")
        self.assertEqual(response_data['lift'][0], "A valid number is required.")

    def test_calculate_dots_returns_error_when_not_provided_required_params(self):
        response = self.client.get(reverse('calculate-dots'), {'female': 'True', 'lift': '100'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data['body'][0], 'This field is required.')

    def test_calculate_dots_returns_200_when_provided_required_params(self):
        response = self.client.get(reverse('calculate-dots'), {'female': 'True', 'lift': 120, 'body': '80'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['result'], 113.07)

    def test_calculate_ipf_gl_logic_returns_valid_data_when_provided_valid_data(self):
        response = Calculators.calculate_ipf_gl_logic(female=True, body=80, lift=120)

        self.assertEqual(response['result'], 23.12)
        self.assertEqual(type(response['result']), float)

    def test_calculate_ipf_gl_returns_400_when_provided_invalid_params_types(self):
        response = self.client.get(reverse('calculate-ipf-gl'), {'female': 'whynot', 'body': 'maybe', 'lift': 'never'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data['female'][0], "Must be a valid boolean.")
        self.assertEqual(response_data['body'][0], "A valid number is required.")
        self.assertEqual(response_data['lift'][0], "A valid number is required.")

    def test_calculate_ipf_gl_returns_error_when_not_provided_required_params(self):
        response = self.client.get(reverse('calculate-ipf-gl'), {'female': 'True', 'lift': '100'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data['body'][0], 'This field is required.')

    def test_calculate_ipf_gl_returns_200_when_provided_required_params(self):
        response = self.client.get(reverse('calculate-ipf-gl'), {'female': 'True', 'lift': 120, 'body': '80'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['result'], 23.12)

    def test_total_logic_returns_valid_data_when_provided_valid_data(self):
        response = Calculators.total_logic(female=False, body=100, sq=200, sq_reps=1,
                                           bp=130, bp_reps=1, dl=240, dl_reps=1)

        self.assertEqual(response['gender'], 'male')
        self.assertEqual(response['squat'], 200)
        self.assertEqual(response['bench_dots'], 80.02)
        self.assertEqual(type(response['total_wilks']), float)

    def test_calculate_total_returns_400_when_provided_invalid_params_types(self):
        response = self.client.get(reverse('calculate-total'), {'female': 'False', 'body': '100', 'sq': 'yes',
                                                                'sq_reps': '1', 'bp': 'maybe', 'bp_reps': '1',
                                                                'dl': 'test', 'dl_reps': '1'})
        response_data = json.loads(response.content)

        self.assertEqual(response_data['sq'][0], "A valid number is required.")
        self.assertEqual(response_data['bp'][0], "A valid number is required.")
        self.assertEqual(response_data['dl'][0], "A valid number is required.")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_calculate_total_returns_error_when_not_provided_required_params(self):
        response = self.client.get(reverse('calculate-total'), {'female': 'False', 'body': '100', 'sq': '200',
                                                                'sq_reps': '1'})
        response_data = json.loads(response.content)

        self.assertEqual(response_data['bp_reps'][0], 'This field is required.')
        self.assertEqual(response_data['dl_reps'][0], 'This field is required.')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_calculate_total_returns_200_when_provided_required_params(self):
        response = self.client.get(reverse('calculate-total'), {'female': 'False', 'body': '100', 'sq': '200',
                                                                'sq_reps': '1', 'bp': '130', 'bp_reps': '1',
                                                                'dl': '240', 'dl_reps': '1'})
        response_data = json.loads(response.content)
        self.assertEqual(response_data['total'], 570.0)
        self.assertEqual(response_data['gender'], 'male')
        self.assertEqual(response_data['bench_wilks'], 94.82)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_GetAllBodyParts_returns_body_parts_list(self):
        response = self.client.get(reverse('read-all-body-parts'))
        response_data = json.loads(response.content)
        self.assertEqual(response_data[0]['name'], 'Triceps')
        self.assertEqual(response_data[1]['id'], 2)

    def test_CreatePrivateExercise_returns_201_when_provided_correct_params(self):
        data = {"name": "Bench Press", "body_part": [1]}
        response = self.client.post(reverse('create-exercise'), data=data, headers=self.auth_header)

        response_data = json.loads(response.content)

        self.assertEqual(response_data['name'], 'Bench Press')
        self.assertEqual(response_data['public'], False)
        self.assertEqual(response_data['user'], 1)
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
        data = self.client.get(reverse('read-private-exercises'),headers=self.auth_header)
        datajson = json.loads(data.content)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

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

    def test_CreateTrainingPlanExerciseInfo_returns_201_when_provided_correct_data(self):
        data = {'exercise': self.public_exercise.pk, 'series': 2, 'reps': 5}
        response = self.client.post(reverse('create-training-plan-exercise-info'), data=data, content_type='application/json',
                                    headers=self.auth_header)
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['series'], 2)

    def test_CreateTrainingPlanExerciseInfo_returns_400_when_not_provided_correct_data(self):
        data = {}
        response = self.client.post(reverse('create-training-plan-exercise-info'), data=data, content_type='application/json',
                                    headers=self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_CreateTrainingPlanExerciseInfo_returns_401_when_authorization_token_not_provided(self):
        data = {}
        response = self.client.post(reverse('create-training-plan-exercise-info'), data=data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ReadTrainingPlanExerciseInfo_returns_200_when_provided_correct_data(self):
        response = self.client.get(reverse('read-training-plan-exercise-info'), headers=self.auth_header)
        response_data = json.loads(response.content)
        self.assertEqual(response_data[0]['reps'], 3)
        self.assertEqual(response_data[0]['exercise'], self.public_exercise.pk)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ReadTrainingPlanExerciseInfo_returns_401_when_not_provided_authorization_token(self):
        response = self.client.get(reverse('read-training-plan-exercise-info'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_UpdateTrainingPlanExerciseInfo_returns_201_when_provided_correct_data(self):
        data = {'reps': 5}
        response = self.client.patch(reverse('update-training-plan-exercise-info', kwargs={'pk': self.exercise_info.pk}), data=data,
                                     headers=self.auth_header, content_type='application/json')
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['reps'], 5)

    def test_UpdateTrainingPlanExerciseInfo_returns_401_when_authorization_token_not_provided(self):
        data = {'reps': 5}
        response = self.client.patch(reverse('update-training-plan-exercise-info', kwargs={'pk': self.exercise_info.pk}), data=data,
                                     content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_DestroyTrainingPlanExerciseInfo_returns_401_when_authorization_token_not_provided(self):
        response = self.client.delete(reverse('delete-training-record', kwargs={'pk': self.exercise_info.pk}),
                                      content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_DestroyTrainingPlanExerciseInfo_returns_204_when_authorization_token_provided(self):
        response = self.client.delete(reverse('delete-training-record', kwargs={'pk': self.exercise_info.pk}),
                                      content_type='application/json',  headers=self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_CreateTrainingExercise_returns_201_when_provided_correct_data(self):
        data = {"series": 3, "reps": 5, "weight": 50, "training": self.training.pk, 'exercise':self.private_exercise.pk}
        response = self.client.post(reverse('create-training-exercise'), data=data, content_type='application/json',
                                    headers=self.auth_header)
        response_data = json.loads(response.content)
        obj = TrainingExercise.objects.last()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response_data['id'], obj.id)
        self.assertEqual(response_data['series'], 3)
        self.assertEqual(response_data['reps'], 5)
        self.assertEqual(response_data['weight'], 50)
        self.assertEqual(response_data['training'], self.training.pk)
        self.assertEqual(response_data['exercise'], self.private_exercise.pk)

    def test_CreateTrainingExercise_returns_400_when_not_provided_correct_data(self):
        data = {}
        response = self.client.post(reverse('create-training-exercise'), data=data, content_type='application/json',
                                    headers=self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_CreateTrainingExercise_returns_401_when_authorization_token_not_provided(self):
        data = {}
        response = self.client.post(reverse('create-training-exercise'), data=data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_ReadTrainingExercise_returns_200_when_provided_correct_data(self):
        response = self.client.get(reverse('read-training-exercise'), headers=self.auth_header)
        response_data = json.loads(response.content)

        self.assertEqual(response_data[0]['training'], self.training.pk)
        self.assertEqual(response_data[0]['reps'], 5)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_ReadTrainingExercise_returns_401_when_not_provided_authorization_token(self):
        response = self.client.get(reverse('read-training-exercise'))

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_UpdateTrainingExercise_returns_201_when_provided_correct_data(self):
        data = {'series': 1}
        response = self.client.patch(reverse('update-training-exercise', kwargs={'pk': self.training_exercise.pk}), data=data,
                                     headers=self.auth_header, content_type='application/json')
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['series'], 1)

    def test_UpdateTrainingExercise_returns_401_when_authorization_token_not_provided(self):
        data = {'series': 1}
        response = self.client.patch(reverse('update-training-exercise', kwargs={'pk': self.training_exercise.pk}), data=data,
                                     content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_DeleteTrainingExercise_returns_401_when_authorization_token_not_provided(self):
        response = self.client.delete(reverse('delete-training-exercise', kwargs={'pk': self.training_exercise.pk}),
                                      content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    def test_DeleteTrainingExercise_returns_204_when_authorization_token_provided(self):
        response = self.client.delete(reverse('delete-training-exercise', kwargs={'pk': self.training_exercise.pk}),
                                      content_type='application/json',  headers=self.auth_header)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)