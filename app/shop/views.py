from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from shop.models import Category, Product, Bucket
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse

from shop.serializers import CategorySerializer, ProductSerializer, CategorySerializerTree, CategorySerializerTreeAdd, \
    BucketPostSerializer


def index(request):
    return HttpResponse('Дратути!')


@csrf_exempt
def product_list(request):
    if request.method == 'GET':
        product = Product.objects.all()
        serializer = ProductSerializer(product, many=True)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = ProductSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@csrf_exempt
def product_list_detail(request, pk):
    try:
        product = Product.objects.get(pk=pk)
    except Product.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        product = Product.objects.get(pk=pk)
        serializer = ProductSerializer(product)
        return JsonResponse(serializer.data, safe=False, json_dumps_params={'ensure_ascii': False})
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = ProductSerializer(product, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)
    elif request.method == 'DELETE':
        product.delete()
        return HttpResponse(status=204)


# @api_view(['GET', 'POST'])
# def category_list_tree(request):
#     if request.method == 'GET':
#         category = Category.objects.filter(parent_category=None)
#         serializer = CategorySerializerTree(category, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CategorySerializerTreeAdd(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryListTree(APIView):
    def get(self, request):
        category = Category.objects.all()
        serializer = CategorySerializerTree(category, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializerTreeAdd(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def category_list_tree_detail(request, pk):
    try:
        category = Category.objects.get(pk=pk)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET':
        serializer = CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class User(APIView):
    def get(self, request):
        user = None
        if request.user.is_authenticated:
            user = request.user.username
        return Response(data={'user': user}, status=status.HTTP_200_OK)


class BucketPost(APIView):
    def post(self, request):
        serializer = BucketPostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            if request.user.is_authenticated:
                bucket, created = Bucket.objects.get_or_create(user=request.user)
                product = get_object_or_404(Product, id=serializer.data.get('product_id'))
                bucket.products.add(product)
                return Response(status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
