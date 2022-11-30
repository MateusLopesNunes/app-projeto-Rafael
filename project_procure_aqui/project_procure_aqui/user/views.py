from rest_framework import viewsets
from .models import User, ListOfProducts
from product.models import State
from .serializers import UserDetailSerializer, UserSerializer, UserUpdateSerializer, UserDeleteSerializer, ListOfProductsSerializer,ListOfProductsDetailSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.contrib.auth.hashers import make_password, check_password


@api_view(['put'])
def update_list_of_products(request, id, products):
    products_format = products.replace('[', '')
    result_format = products_format.replace(']', '')
    product_array = result_format.split(", ")
    list_int = list(map(int, product_array))

    x = ListOfProducts.objects.raw('SELECT * FROM user_listofproducts as list_p where id = ' + str(id))
    list_p = x[0]
    list_p.products.set(list_int)

    list_p.save()
    return Response(status=status.HTTP_201_CREATED)


@api_view(['delete'])
def delete_product_in_list_of_products(request, id):

    x = ListOfProducts.objects.raw('SELECT * FROM user_listofproducts as list_p where id = ' + str(id))
    list_p = x[0]

    list_p.save()
    return Response(status=status.HTTP_201_CREATED)


@api_view(['get'])
def validate_user(request, id, email, password):
    user = User.object.get(id=id)
    
    validate_password = check_password(password=password, encoded=user.password)

    if user.email == email and validate_password:
        return Response({'is_product': True})

    return Response({'is_product': False})
 

class UserViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticated,)
    queryset = User.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', 'email']

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserSerializer
        elif self.action == 'update' or self.action == 'partial_update': 
            return UserUpdateSerializer
        elif self.action == 'delete':
            return UserDeleteSerializer

    def perform_create(self, serializer):
        print(serializer)
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()     

    def perform_update(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class ListOfProductsViewSet(viewsets.ModelViewSet):
    #permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = ListOfProducts.objects.all()
    #serializer_class = ListOfProductsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ListOfProductsDetailSerializer
        return ListOfProductsSerializer

    def update(self, request, *args, **kwargs):
        return ListOfProducts.objects.update(request.data)

    def create(self, request):
        products = request.data.get('products')
        products_format = products.replace('[', '')
        result_format = products_format.replace(']', '')
        #product_array = result_format.split(" ")
        list_int = int(result_format)
        newlist = []
        newlist.append(list_int)
        print(newlist)

        user = User.objects.filter(id=request.data.get('user'))[0]
        list_of_products = ListOfProducts.objects.create(user=user)
        list_of_products.products.set(newlist)
        
        return Response(status=status.HTTP_201_CREATED)