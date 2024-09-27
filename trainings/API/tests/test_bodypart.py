from django.test import TestCase
from django.urls import reverse
import json
from trainings.models import BodyPart

class TestBodyPartApi(TestCase):
    @classmethod
    def setUpTestData(cls):
        BodyPart.objects.create(name='Triceps')
        BodyPart.objects.create(name='Biceps')

    def test_GetAllBodyParts_returns_body_parts_list(self):
        response = self.client.get(reverse('api-read-all-body-parts'))
        response_data = json.loads(response.content)
        self.assertEqual(response_data[0]['name'], 'Triceps')
        self.assertEqual(response_data[1]['id'], 2)
