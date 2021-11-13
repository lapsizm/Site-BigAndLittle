from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import BaseView, ProductList, ProductDetail, CategoryDetail, DynamicProductLoad


urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('products/', ProductList, name='product_list'),
    path('products/<str:category_slug>/', CategoryDetail, name='category_detail'),
    path('products/<str:category_slug>/<str:product_slug>/', ProductDetail, name='product_detail'),
    path('load-more-products/', DynamicProductLoad.as_view(), name='load-more-products')
]
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)