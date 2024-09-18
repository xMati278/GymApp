from django.test import TestCase
from django.urls import reverse
import json
from trainings.calculators import Calculators
from rest_framework import status


class TestCalculatorApi(TestCase):
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
