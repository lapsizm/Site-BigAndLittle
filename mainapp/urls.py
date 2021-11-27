from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from .views import *


urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('products/', ProductList, name='product_list'),
    path('products/<str:category_slug>/', CategoryDetail, name='category_detail'),
    path('products/<str:category_slug>/<str:product_slug>/', ProductDetail, name='product_detail'),
    path('load-more-products/', DynamicProductLoad.as_view(), name='load-more-products'),
    path('personal_area/', PersonalArea, name='personal_area'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='base'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration')

    # path('cart/', CartView.as_view(), name='cart'),
    # path('add-to-cart/<str:product_slug>/', AddToCartView.as_view(), name='add-to-cart'),
    # path('delete-from-cart/<str:product_slug>/', DeleteFromCart.as_view(), name='delete-from-cart'),
    # path('change-specification/<str:product_slug>/', ChangeSpecification.as_view(), name='change-specification'),

]
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)