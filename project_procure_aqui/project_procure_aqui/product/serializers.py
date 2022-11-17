from dataclasses import fields
from itertools import product
from traceback import print_tb
from .models import Product, Category, City, HistoricPrice, State, Supermarket
from rest_framework import serializers

#somente get      
class CategoryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

#somente get
class CityDetailSerializer(serializers.ModelSerializer):
    state = serializers.ReadOnlyField(source='state.state_name')
    class Meta:
        model = City
        fields = ['id', 'city_name', 'state']

#somente get
class SupermarketDetailSerializer(serializers.ModelSerializer):
    city = CityDetailSerializer()
    class Meta:
        model = Supermarket
        fields = '__all__'


#post, put, delete
class HistoricPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricPrice
        fields = '__all__'

#update
class HistoricPriceUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricPrice
        fields = ['price']

    #def update(self, instance, validated_data):
    #    instance.price = validated_data.get('price', instance.price)
    #    instance.save()
    #    return instance


#post, put, delete
class ProductSerializer(serializers.ModelSerializer):
    #historic_price = HistoricPriceSerializer()
    class Meta:
        model = Product
        exclude = ['is_visible', 'image_url']

    '''def create(self, validated_data):
        supermarket = validated_data.pop('supermarket')
        product_instance = Product.objects.create(**validated_data)
        product_instance.supermarket.set(supermarket)
        return product_instance'''

#get
class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.category_name')
    supermarket = SupermarketDetailSerializer()
    class Meta:
        model = Product
        fields = '__all__'
        depth = 5

#somente get
class StateDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

#get
class ProductResponseSerializer(serializers.ModelSerializer):
    category = serializers.ReadOnlyField(source='category.category_name')
    class Meta:
        model = Product
        exclude = ['image_url']
        depth = 5


#get
class HistoricPriceDetailSerializer(serializers.ModelSerializer):
    product = ProductResponseSerializer()
    class Meta:
        model = HistoricPrice
        fields = '__all__'
        depth = 5
