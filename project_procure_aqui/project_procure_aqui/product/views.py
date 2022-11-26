from itertools import product
from math import prod
from traceback import print_tb
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .models import Product, Category, City, HistoricPrice, State, Supermarket
from .serializers import HistoricPriceDetailSerializer, HistoricPriceUpdateSerializer, ProductSerializer, ProductDetailSerializer, CategoryDetailSerializer, CityDetailSerializer, HistoricPriceSerializer, StateDetailSerializer, SupermarketDetailSerializer
from user.serializers import CitySerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser
from product import serializers
from product import models
from django_filters.rest_framework import DjangoFilterBackend
import math

 
@api_view(['GET'])
@parser_classes([JSONParser])
def find_bar_code(request, code, id, format=None):
    supermarket = Supermarket.objects.filter(id=id)

    if len(supermarket) == 0:
        print('entrou')
        return Response(status=status.HTTP_404_NOT_FOUND)

    product_in_supermaket = Product.objects.filter(supermarket=supermarket[0])

    if product_in_supermaket:
        product = Product.objects.filter(bar_code=code)
        if product:
            return Response({'id': product[0].id, 'is_product': True})
        else:
            return Response({'is_product': False})


'''Agora funciona'''
@api_view(['GET'])
def filter_city_per_state(request, id):
    state = State.objects.get(id=id)
    city = City.objects.filter(state=state)
    serializer = CitySerializer(city, many=True)
    return Response(serializer.data ,status=status.HTTP_200_OK)
   

@api_view(['POST'])    
def update_product(request, code):
    serializer = HistoricPriceUpdateSerializer(data=request.data)
    if serializer.is_valid():
        product = Product.objects.get(id=code)
        if product:
            price = request.data.get("price")
            print(price)
            supermarket = product.supermarket
            print(supermarket)
            historicPrice = HistoricPrice.objects.create(product=product, price=price, supermarket=supermarket[0])
            serializer = HistoricPriceSerializer(data=historicPrice)
            if serializer.is_valid():
                serializer.save()
                print(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Product.objects.order_by('-creation_date_product').filter(is_visible=True)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['category', 'product_name', 'bar_code']

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ProductDetailSerializer
        elif self.action == 'create' or self.action == 'update' or self.action == 'partial_update': 
            return ProductSerializer
    
    def create(self, request, *args, **kwargs):
        create = super().create(request)
        product = Product.objects.get(id=create.data.get('id'))
        print(product)
        supermarket = product.supermarket
        print(supermarket)
        HistoricPrice.objects.create(product=product, price=product.price, supermarket=supermarket)
        return create
    
    def update_and_create_historic(self, data, request):
        instance = super().update(request)
        product = data.get_object()
        HistoricPrice.objects.create(product=product, price=product.price, supermarket=product.supermarket)
        return instance

    def update(self, request, pk=None):
        historic_prices = HistoricPrice.objects.filter(product=pk)

        if historic_prices.count() < 5:
            instance = super().update(request)
            product = self.get_object()
            HistoricPrice.objects.create(product=product, price=product.price, supermarket=product.supermarket)
            return instance
 
        sum = 0.0
        for historic_price in historic_prices:
           sum += historic_price.price

        average = sum/historic_prices.count()    
        x = 0.0
        for historic_price in historic_prices:
           x += abs((historic_price.price - average) * 2)

        result = math.sqrt(x / historic_prices.count() - 1)
        x = average + result
        y = average - result

        price = float(request.data.get('price'))

        if price <= (average + result) and price >= (average - result):
            instance = super().update(request)
            product = self.get_object()
            HistoricPrice.objects.create(product=product, price=product.price, supermarket=product.supermarket)
            return instance
        else:
            return Response({'Error': 'o valor apresentado está discrepante a média de preços deste produto'})
        

class CategoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Category.objects.all()
    serializer_class = CategoryDetailSerializer

class CityViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = City.objects.all()
    serializer_class = CityDetailSerializer

class StateViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = State.objects.all()
    serializer_class = StateDetailSerializer

class SupermarketViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Supermarket.objects.all()
    serializer_class = SupermarketDetailSerializer

class HistoricPriceViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = HistoricPrice.objects.all()
    #serializer_class = HistoricPriceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['product']

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return HistoricPriceDetailSerializer
        elif self.action == 'create': 
            return HistoricPriceSerializer
        elif self.action == 'update' or self.action == 'partial_update':
            return HistoricPriceUpdateSerializer
