from shop.models import Category
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from shop.serializers import CategorySerializer


def index(request):
    return HttpResponse('Дратути!')


def category_list(request):
    if request.method == 'GET':
        category = Category.objects.all()
        serializer = CategorySerializer(category, many=True)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})

# Create your views here.
