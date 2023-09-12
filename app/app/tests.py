from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from shop.models import Category, Product, Bucket
from rest_framework.test import APITestCase

from django.contrib.auth.models import User


# class CategoryTestCase(TestCase):
#     def setUp(self):
#         Category.objects.create(name='Категория 4',
#                                 parent_category=None
#                                 )
#
#     def test_create(self):
#         new_category = Category.objects.get(name='Категория 4')
#         self.assertEqual(new_category.name, 'Категория 4')
#         # print(new_category.name)
#         # print(Category.objects.count())
#
#
# class UserTestCase(APITestCase):
#     def test_user(self):
#         User.objects.create_user(username='admin', password='admin')
#         self.assertTrue(self.client.login(username='admin', password='admin'))
#         url = reverse('user')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, {'user': 'admin'})
#
#     def test_user_no_auth(self):
#         User.objects.create_user(username='admin', password='admin')
#         url = reverse('user')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data, {'user': None})


class BucketTestCase(APITestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='test', password='test')
        self.user2 = User.objects.create_user(username='test1', password='test1')
        category = Category.objects.create(name='Категория 1', parent_category=None)
        self.products = [Product.objects.create(name=f'Товар {i}', category=category) for i in range(1, 5)]
        print(self.products)

    def test_bucket(self):
        self.assertTrue(self.client.login(username='test1', password='test1'))
        url = reverse('bucket')
        for product in self.products[:2:]:
            response = self.client.post(url, {'product_id': product.id})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user2.bucket.products.count(), 2)

        self.assertTrue(self.client.login(username='test', password='test'))
        url = reverse('bucket')
        for product in self.products[2::]:
            response = self.client.post(url, {'product_id': product.id})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user1.bucket.products.count(), 2)
