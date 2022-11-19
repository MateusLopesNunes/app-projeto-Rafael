from rest_framework import viewsets
from .models import User, ListOfProducts
from product.models import State
from .serializers import UserDetailSerializer, UserSerializer, UserUpdateSerializer, ListOfProductsSerializer,ListOfProductsDetailSerializer
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters


# @api_view(['GET'])    
# def filter_with_email(request, email):
#     users = User.objects.filter(email=email)
#     user = users[0]
#     serializer = UserDetailSerializer(user)
#     if user:
#         return Response(serializer.data ,status=status.HTTP_200_OK)
#     else:
#         return Response(status=status.HTTP_404_NOT_FOUND)


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
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = ListOfProducts.objects.all()
    #serializer_class = ListOfProductsSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['user']

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'retrieve':
            return ListOfProductsDetailSerializer
        return ListOfProductsSerializer