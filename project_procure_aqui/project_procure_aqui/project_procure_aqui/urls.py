from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from product import views as viewsProduct
from user import views as viewsUser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt.models import TokenUser

router = routers.DefaultRouter()
router.register("products", viewsProduct.ProductViewSet, basename="products")
router.register("categories", viewsProduct.CategoryViewSet, basename="categories")
router.register("citys", viewsProduct.CityViewSet, basename="citys")
router.register("states", viewsProduct.StateViewSet, basename="states")
router.register("supermarkets", viewsProduct.SupermarketViewSet, basename="supermarkets")
router.register("historicPrices", viewsProduct.HistoricPriceViewSet, basename="historicPrices")
router.register("users", viewsUser.UserViewSet, basename="users")
router.register("listOfProducts", viewsUser.ListOfProductsViewSet, basename="listOfProducts")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('bar_code/<int:code>/supermarket/<int:id>', viewsProduct.find_bar_code),
    path('products/<int:code>/update', viewsProduct.update_product),
    path('citys/<int:id>/filter', viewsProduct.filter_city_per_state),
    path('validateUser/<int:id>/email/<str:email>/password/<str:password>', viewsUser.validate_user),
    #path('users/filter/<str:email>', viewsUser.filter_with_email),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
