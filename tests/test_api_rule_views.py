import json

from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from api import serializers

from api.models import Brand, Rule
from api.serializers import RuleSerializer


class TestBrandsListView(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_get_all_rules(self):
        brand = Brand.objects.create(name='Brand1')
        rule1 = Rule.objects.create(description='A description', type_of_search='contains', pattern='[0-9]', column='category')
        rule2 = Rule.objects.create(description='Another description', type_of_search='contains', pattern='[0-9]', column='name')
        rule1.brands.add(brand)
        rule2.brands.add(brand)
        response = self.client.get(reverse('create-list-rules'))
        rules = Rule.objects.all()
        serializer = RuleSerializer(rules, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
