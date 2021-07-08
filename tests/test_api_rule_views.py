from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from api.models import Brand, Rule
from api.serializers import RuleSerializer


class TestBrandsListView(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.brand1 = Brand.objects.create(name='New brand')
        self.brand2 = Brand.objects.create(name='Second brand')

    def test_get_all_rules(self):
        rule1 = Rule.objects.create(description='A description', type_of_search='contains', pattern='[0-9]', column='category')
        rule2 = Rule.objects.create(description='Another description', type_of_search='contains', pattern='[0-9]', column='name')
        rule1.brands.add(self.brand1)
        rule2.brands.add(self.brand1)
        response = self.client.get(reverse('create-list-rules'))
        rules = Rule.objects.all()
        serializer = RuleSerializer(rules, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_method_adds_new_rule(self):
        rule = {
            "description":"some description", 
            "type_of_search":"contains", 
            "pattern":"Extras", 
            "column":"category", 
            "brands":[self.brand1.id, self.brand2.id]
        }
        response = self.client.post(reverse('create-list-rules'), data=rule, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_post_method_fails_to_add_new_rule(self):
        rule = {
            "wrong field name":"some description", 
            "type_of_search":"contains", 
            "pattern":"Extras", 
            "column":"category", 
            "brands":[self.brand1.id, self.brand2.id]
        }
        response = self.client.post(reverse('create-list-rules'), data=rule, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestRuleDetailView(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.rule1 = Rule.objects.create(description='A description', type_of_search='contains', pattern='[0-9]', column='category')
        
    def test_get_valid_single_rule(self):
        response = self.client.get(reverse('detail-update-delete-rule', kwargs={'id': self.rule1.id}))
        rule1 = Rule.objects.get(id=self.rule1.id)
        serializer = RuleSerializer(rule1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_rule(self):
        response = self.client.get(reverse('detail-update-delete-rule', kwargs={'id': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_update_rule(self):
        brand = Brand.objects.create(name="Brand 1")
        response = self.client.put(
            reverse('detail-update-delete-rule', 
            kwargs={'id': self.rule1.id}), 
            data={
                    "description":"Updated description", 
                    "type_of_search":"contains", 
                    "pattern":"Extras", 
                    "column":"category", 
                    "brands":[brand.id]
            }, 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_rule(self):
        response = self.client.put(
            reverse('detail-update-delete-rule', 
            kwargs={'id': self.rule1.id}),
            data={
                    "description":"Updated description", 
                    "type_of_search":"contains", 
                    "pattern":"Extras", 
                    "column":"category", 
                    "brands":[55]
            }, 
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_delete_rule(self):
        response = self.client.delete(reverse('detail-update-delete-rule', kwargs={'id': self.rule1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)