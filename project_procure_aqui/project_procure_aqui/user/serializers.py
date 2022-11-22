from random import choices
from .models import ListOfProducts, User, City
from product.models import State
from rest_framework import serializers
from product.serializers import CityDetailSerializer, ProductDetailSerializer


#get
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'

#get
class UserDetailSerializer(serializers.ModelSerializer):
    city = CityDetailSerializer()
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'sex', 'birth_date', 'city']

#post, put, delete
class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = '__all__'

#post, put, delete
class UserSerializer(serializers.ModelSerializer): 
    sexEnum = (
        ("masculine", "Masculino"),
        ("feminine", "feminino"),
        ("other", "outro"),
    )

    birth_date = serializers.DateField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'sex', 'birth_date', 'city']

class UserUpdateSerializer(serializers.ModelSerializer): 
    sexEnum = (
        ("masculine", "Masculino"),
        ("feminine", "feminino"),
        ("other", "outro"),
    )

    birth_date = serializers.DateField()
    class Meta:
        model = User
        fields = ['username', 'email', 'sex', 'birth_date', 'city']


#get
class ListOfProductsDetailSerializer(serializers.ModelSerializer):
    products = serializers.ManyRelatedField(ProductDetailSerializer())
    user = UserDetailSerializer()
    class Meta:
        model = ListOfProducts
        fields = '__all__'
        depth = 5

#post, put, delete
class ListOfProductsSerializer(serializers.ModelSerializer):
    products = serializers.CharField(max_length=100)
    class Meta:
        model = ListOfProducts
        fields = '__all__'