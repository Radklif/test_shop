import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# class Question(models.Model):
#     question_test = models.CharField(max_length=100)
#     pub_date = models.DateTimeField('Date pub')
#
#     def __str__(self):
#         return self.question_test
#
#     def was_published_recently(self):
#         return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
#
#
# class Choice(models.Model):
#     question = models.ForeignKey(Question, on_delete=models.CASCADE)
#     choice_text = models.CharField(max_length=100)
#     votes = models.IntegerField(default=0)
#
#     def __str__(self):
#         return self.choice_text

class Category(models.Model):
    name = models.CharField(max_length=200)
    parent_category = models.ForeignKey('self', on_delete=models.CASCADE, null=True, related_name='children')


class Product(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')


class Bucket(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bucket')
    products = models.ManyToManyField(Product)


class Order(models.Model):
    product = models.ManyToManyField(Product)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

# Create your models here.
