from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status

from api.models import Brand
from api.serializers import BrandSerializer


class TestBrandsListView(TestCase):
    
    def setUp(self):
        self.client = Client()

    def test_get_all_brands(self):
        Brand.objects.bulk_create(
            [
                Brand(name='Test Brand 1'), 
                Brand(name='Test Brand 2')
            ]
        )
        response = self.client.get(reverse('create-list-brands'))
        brands = Brand.objects.all()
        serializer = BrandSerializer(brands, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_method_adds_new_brand(self):
        brand = {"name": "New brand"}
        response = self.client.post(reverse('create-list-brands'), data=brand, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_method_fails_to_add_new_brand(self):
        brand = {"nme": "New brand"}
        response = self.client.post(reverse('create-list-brands'), data=brand, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class TestBrandDetailView(TestCase):

    def setUp(self):
        self.client = Client()
        self.brand1 = Brand.objects.create(name='Test Brand 1')
        self.brand2 = Brand.objects.create(name='Test Brand 2')
        
    def test_get_valid_single_brand(self):
        response = self.client.get(reverse('detail-update-delete-brand', kwargs={'id': self.brand1.id}))
        brand1 = Brand.objects.get(id=self.brand1.id)
        serializer = BrandSerializer(brand1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_invalid_single_brand(self):
        response = self.client.get(reverse('detail-update-delete-brand', kwargs={'id': 30}))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_valid_update_brand(self):
        response = self.client.put(
            reverse('detail-update-delete-brand', 
            kwargs={'id': self.brand1.id}), 
            data={"name": "Updated brand1"}, content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_update_brand(self):
        response = self.client.put(
            reverse('detail-update-delete-brand', 
            kwargs={'id': self.brand2.id}),
            data={"name": "Test Brand 1"},
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_valid_delete_brand(self):
        response = self.client.delete(reverse('detail-update-delete-brand', kwargs={'id': self.brand1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)