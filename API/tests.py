from django.test import TestCase
from django.urls import reverse
import json
from http import HTTPStatus
from .calculators import Calculators
# Create your tests here.


class TestApi(TestCase):
    def test_validate_calculator_data_returns_error_when_provided_invalid_params_types(self):
        response = Calculators.validate_calculator_data(lifted_weight='test', reps='15s', one_rm_calc=True)

        self.assertEqual(response['error'], 'Invalid parameter types.')

    def test_validate_calculator_data_returns_error_when_not_provided_required_params(self):
        response = Calculators.validate_calculator_data(lifted_weight='150', is_female='True')

        self.assertEqual(response['error'], 'Missing required parameters.')

    def test_validate_calculator_data_returns_valid_data_with_valid_types_when_provided_valid_data(self):
        response = Calculators.validate_calculator_data(lifted_weight='150', is_female='True', body_weight='100')

        self.assertEqual(type(response['lifted_weight']), float)
        self.assertEqual(type(response['is_female']), bool)
        self.assertEqual(response['body_weight'], 100)

    def test_calculate_1rm_logic_returns_valid_data_when_provided_valid_data(self):
        few_reps_response = Calculators.calculate_1rm_logic(lifted_weight=100, reps=5)
        one_rep_response = Calculators.calculate_1rm_logic(lifted_weight=100, reps=1)

        self.assertEqual(few_reps_response, 115)
        self.assertEqual(one_rep_response, 100)

    def test_calculate_1rm_returns_400_when_provided_invalid_params_types(self):
        response = self.client.get(reverse('calculate-1rm'), {'reps': 'asd', 'weight': '100'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response_data['error'],
                         'Invalid parameter types.')

    def test_calculate_1rm_returns_error_when_not_provided_required_params(self):
        response = self.client.get(reverse('calculate-1rm'), {'reps': '5'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response_data['error'], 'Missing required parameters.')

    def test_calculate_1rm_returns_200_when_provided_valid_data(self):
        response = self.client.get(reverse('calculate-1rm'), {'reps': '7', 'weight': '100'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response_data['1rm'], 121)

    def test_calculate_wilks_logic_returns_valid_data_when_provided_valid_data(self):
        response = Calculators.calculate_wilks_logic(is_female=True, body_weight=80, lifted_weight=120)

        self.assertEqual(response, 135.81)
        self.assertEqual(type(response), float)

    def test_calculate_wilks_returns_400_when_provided_invalid_params_types(self):
        response = self.client.get(reverse('calculate-wilks'), {'female': 'yes', 'body': 'maybe', 'lift': '100'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response_data['error'],
                         'Invalid parameter types.')

    def test_calculate_wilks_returns_error_when_not_provided_required_params(self):
        response = self.client.get(reverse('calculate-wilks'), {'female': 'True', 'lift': '100'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response_data['error'], 'Missing required parameters.')

    def test_calculate_wilks_returns_200_when_provided_valid_data(self):
        response = self.client.get(reverse('calculate-wilks'), {'female': 'True', 'lift': 120, 'body': '80'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response_data['wilks'], 135.81)

    def test_calculate_dots_logic_returns_valid_data_when_provided_valid_data(self):
        response = Calculators.calculate_dots_logic(is_female=True, body_weight=80, lifted_weight=120)

        self.assertEqual(response, 113.07)
        self.assertEqual(type(response), float)

    def test_calculate_dots_returns_400_when_provided_invalid_params_types(self):
        response = self.client.get(reverse('calculate-dots'), {'female': 'yes', 'body': 'maybe', 'lift': '100'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response_data['error'],
                         'Invalid parameter types.')

    def test_calculate_dots_returns_error_when_not_provided_required_params(self):
        response = self.client.get(reverse('calculate-dots'), {'female': 'True', 'lift': '100'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response_data['error'], 'Missing required parameters.')

    def test_calculate_dots_returns_200_when_not_provided_required_params(self):
        response = self.client.get(reverse('calculate-dots'), {'female': 'True', 'lift': 120, 'body': '80'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response_data['dots'], 113.07)

    def test_calculate_ipf_gl_logic_returns_valid_data_when_provided_valid_data(self):
        response = Calculators.calculate_ipf_gl_logic(is_female=True, body_weight=80, lifted_weight=120)

        self.assertEqual(response, 23.12)
        self.assertEqual(type(response), float)

    def test_calculate_ipf_gl_returns_400_when_provided_invalid_params_types(self):
        response = self.client.get(reverse('calculate-ipf-gl'), {'female': 'yes', 'body': 'maybe', 'lift': '100'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response_data['error'],
                         'Invalid parameter types.')

    def test_calculate_ipf_gl_returns_error_when_not_provided_required_params(self):
        response = self.client.get(reverse('calculate-ipf-gl'), {'female': 'True', 'lift': '100'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)
        self.assertEqual(response_data['error'], 'Missing required parameters.')

    def test_calculate_ipf_gl_returns_200_when_not_provided_required_params(self):
        response = self.client.get(reverse('calculate-ipf-gl'), {'female': 'True', 'lift': 120, 'body': '80'})
        response_data = json.loads(response.content)

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertEqual(response_data['ipf_gl'], 23.12)

    def test_total_logic_returns_valid_data_when_provided_valid_data(self):
        response = Calculators.total_logic(is_female=False, body_weight=100, squat_weight=200, squat_reps=1, bench_weight=130,
                               bench_reps=1, deadlift_weight=240, deadlift_reps=1)

        self.assertEqual(response['gender'], 'male')
        self.assertEqual(response['squat'], 200)
        self.assertEqual(response['bench_dots'], 80.02)
        self.assertEqual(type(response['total_wilks']), float)

    def test_validate_total_data_returns_error_when_provided_invalid_params_types(self):
        response = Calculators.validate_total_data(is_female='female', body_weight='100', squat_weight='200', squat_reps='1',
                                       bench_weight='130', bench_reps='1', deadlift_weight='no', deadlift_reps='1')

        self.assertEqual(response['error'], 'Invalid parameter types.')

    def test_validate_total_data_returns_error_when_not_provided_required_params(self):
        response = Calculators.validate_total_data(is_female='False', body_weight='100', squat_weight='200', squat_reps='1',
                                       bench_weight='130', bench_reps='1')

        self.assertEqual(response['error'], 'Missing required parameters.')

    def test_validate_total_data_returns_valid_data_with_valid_types_when_provided_valid_data(self):
        response = Calculators.validate_total_data(is_female='False', body_weight='100', squat_weight='200', squat_reps='1',
                                       bench_weight='130', bench_reps='1', deadlift_weight='240', deadlift_reps='1')

        self.assertEqual(response['squat_weight'], 200)
        self.assertEqual(response['bench_weight'], 130)

    def test_calculate_total_returns_400_when_provided_invalid_params_types(self):
        response = self.client.get(reverse('calculate-total'), {'female': 'False', 'body': '100', 'sq': 'yes',
                                                                'sq-reps': '1', 'bp': 'maybe', 'bp-reps': '1',
                                                                'dl': 'test', 'dl-reps': '1'})
        response_data = json.loads(response.content)

        self.assertEqual(response_data['error'], 'Invalid parameter types.')
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_calculate_total_returns_error_when_not_provided_required_params(self):
        response = self.client.get(reverse('calculate-total'), {'female': 'False', 'body': '100', 'sq': '200',
                                                                'sq-reps': '1'})
        response_data = json.loads(response.content)

        self.assertEqual(response_data['error'], 'Missing required parameters.')
        self.assertEqual(response.status_code, HTTPStatus.BAD_REQUEST)

    def test_calculate_total_returns_200_when_not_provided_required_params(self):
        response = self.client.get(reverse('calculate-total'), {'female': 'False', 'body': '100', 'sq': '200',
                                                                'sq-reps': '1', 'bp': '130', 'bp-reps': '1',
                                                                'dl': '240', 'dl-reps': '1'})
        response_data = json.loads(response.content)

        self.assertEqual(response_data['total'], 570.0)
        self.assertEqual(response_data['gender'], 'male')
        self.assertEqual(response_data['bench_wilks'], 94.82)
        self.assertEqual(response.status_code, HTTPStatus.OK)
