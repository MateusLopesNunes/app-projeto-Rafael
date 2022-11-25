from django.contrib import admin
from .models import User, ListOfProducts

class UserAdmin(admin.ModelAdmin):
    exclude = ['first_name', 'last_name', 'groups', 'user_permissions', 'last_login', 'is_staff', 'is_superuser', 'date_joined']
    list_display = ('id', 'username', 'email', 'sex', 'birth_date', 'city', 'date_joined', 'is_active') #coloca os campos na tabela
    list_display_links = ('id', 'username') #vira links
    search_fields = ('username',) #cria uma pesquisa
    list_per_page = 5 #cria paginação

    def set_password(self):
        self

class ListOfProductsAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',) #coloca os campos na tabela
    list_display_links = ('id', 'user') #vira links
    search_fields = ('user',) #cria uma pesquisa
    list_per_page = 5 #cria paginação


admin.site.register(User, UserAdmin)
admin.site.register(ListOfProducts, ListOfProductsAdmin)
