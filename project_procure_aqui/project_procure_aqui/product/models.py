from itertools import product
from django.db import models

class State(models.Model):
    state_name = models.CharField(max_length=45)
    def __str__(self):
        return self.state_name

class City(models.Model):
    city_name = models.CharField(max_length=45)
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    def __str__(self):
        return self.city_name

class Category(models.Model):
    category_name = models.CharField(max_length=45)
    def __str__(self):
        return self.category_name

class Supermarket(models.Model):
    supermarket_name = models.CharField(max_length=60)
    street = models.CharField(max_length=60)
    district = models.CharField(max_length=60)
    complement = models.CharField(max_length=80, blank=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.supermarket_name

class Product(models.Model):
    product_name = models.CharField(max_length=100)
    bar_code = models.IntegerField()
    image_url = models.ImageField(upload_to='fotos/%d/%m/%Y', blank=True, null=True, default='fotos/default/índice.png')
    creation_date_product  = models.DateTimeField(auto_now_add=True)
    update_date_product = models.DateTimeField(auto_now=True)
    is_visible = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.product_name + " " + str(self.pk)

'''class ProductSupermarket(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE)
'''

class HistoricPrice(models.Model):
    price = models.FloatField()
    alteration_date = models.DateTimeField(auto_now_add=True)
    supermarket = models.ForeignKey(Supermarket, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product',null=True,blank=True)
