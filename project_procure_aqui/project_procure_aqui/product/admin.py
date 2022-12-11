from django.contrib import admin
from .models import Product, Category, Supermarket, State, City, HistoricPrice

class StateAdmin(admin.ModelAdmin):
    list_display = ('id', 'state_name') #coloca os campos na tabela
    list_display_links = ('id', 'state_name') #vira links
    search_fields = ('state_name',) #cria uma pesquisa
    list_per_page = 10 #cria paginação


class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'city_name', "state") #coloca os campos na tabela
    list_display_links = ('id', 'city_name') #vira links
    search_fields = ('city_name',) #cria uma pesquisa
    list_per_page = 10 #cria paginação


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'category_name') #coloca os campos na tabela
    list_display_links = ('id', 'category_name') #vira links
    search_fields = ('category_name',) #cria uma pesquisa
    list_per_page = 10 #cria paginação


class SupermarketAdmin(admin.ModelAdmin):
    list_display = ('id', 'supermarket_name', 'street', 'district', 'complement', 'city') #coloca os campos na tabela
    list_display_links = ('id', 'supermarket_name') #vira links
    search_fields = ('supermarket_name',) #cria uma pesquisa
    list_per_page = 10 #cria paginação


class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'product_name', 'bar_code', 'image_url', 'is_visible', 'category', 'supermarket'] #coloca os campos na tabela
    list_display_links = ('id', 'product_name') #vira links
    search_fields = ('product_name', 'bar_code') #cria uma pesquisa
    list_filter = ('category', 'is_visible') #filtra
    list_editable = ('is_visible',)
    list_per_page = 10 #cria paginação


class HistoricPriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'price', 'alteration_date', 'supermarket', 'product') #coloca os campos na tabela
    list_display_links = ('id', 'price') #vira links
    search_fields = ('price',) #cria uma pesquisa
    list_filter = ('product',) #filtra
    list_per_page = 10 #cria paginação


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Supermarket, SupermarketAdmin)
admin.site.register(State, StateAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(HistoricPrice, HistoricPriceAdmin)