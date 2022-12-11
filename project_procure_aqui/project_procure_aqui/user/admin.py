from django.contrib import admin
from .models import User, ListOfProducts


class ListOfProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',) #coloca os campos na tabela
    list_display_links = ('id', 'user') #vira links
    search_fields = ('user',) #cria uma pesquisa
    list_per_page = 5 #cria paginação


admin.site.register(ListOfProducts, ListOfProductsAdmin)
