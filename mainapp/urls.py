from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from .views import *

urlpatterns = [
    path('', BaseView.as_view(), name='base'),
    path('products/', ProductList.as_view(), name='product_list'),
    path('products/<str:category_slug>/', CategoryDetail.as_view(), name='category_detail'),
    path('products/<str:category_slug>/<str:product_slug>/', ProductDetail.as_view(), name='product_detail'),

    path('load-more-products/', DynamicProductLoad.as_view(), name='load-more-products'),

    path('personal_area/', AccountView.as_view(), name='personal_area'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='base'), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('personal-info/', PersonalData.as_view(), name='personal_info'),
    path('history-orders/', HistoryOrders.as_view(), name='history_orders'),
    path('history-detail/<str:id>', HistoryDetail.as_view(), name='history_detail'),
    path('change-info/', ChangeInfo.as_view(), name='change_info'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/<str:product_slug>/', AddToCartView.as_view(), name='add_to_cart'),
    path('delete-from-cart/<str:product_slug>/<str:size>/<str:color>/<int:qty>/', DeleteFromCart.as_view(),
         name='delete_from_cart'),
    path('change-qty/<str:product_slug>/<str:size>/<str:color>', ChangeQTY.as_view(), name='change_qty'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('make-order/', MakeOrderView.as_view(), name='make_order'),
    path('payment/<str:id>/', Payment.as_view(), name='payment'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
         name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
         name="password_reset_done"),
    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
         name="password_reset_confirm"),
    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),
         name="password_reset_complete"),

]
# ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
