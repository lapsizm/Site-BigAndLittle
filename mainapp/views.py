from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.views import View
from django import views
from .models import *
from django.http import JsonResponse, HttpResponseRedirect
from .forms import *
from django.contrib.auth import authenticate, login

class BaseView(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'base.html', {})


def PersonalArea(request):
    return render(request, 'personal_area.html', {})


def ProductList(request):
    categories = Category.objects.all()
    products = Product.objects.all()[:9]
    images = []
    for product in products:
        images.append(get_object_or_404(ImageGallery, object_id=product.id, is_main=True))

    return render(request, 'catalog.html', locals())


def CategoryDetail(request, category_slug):
    categories = Category.objects.all()
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category__slug=category_slug)
    images = ImageGallery.objects.all()
    return render(request, 'category_detail.html', locals())


def ProductDetail(request, category_slug, product_slug):
    categories = Category.objects.all()
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=product_slug)
    images = ImageGallery.objects.filter(object_id=product.id)
    main_image = get_object_or_404(ImageGallery, object_id=product.id, is_main=True)
    colors = ColorField.objects.filter(object_id=product.id)
    sizes = SizeField.objects.filter(object_id=product.id)
    return render(request, 'product_detail.html', locals())


class DynamicProductLoad(View):
    def get(self, request, *args, **kwargs):
        last_product_id = request.GET.get('lastProductId')
        more_products = Product.objects.filter(pk__gt=int(last_product_id)).values('id', 'title', 'price',
                                                                                   'description')[:9]
        images = ImageGallery.objects.filter(object_id=last_product_id, is_main=True)

        if not more_products:
            return JsonResponse({'data': False})
        data = []
        main_img = []
        for img in images:
            main_img.append('{{img.image.url}}')
            break

        for product in more_products:
            obj = {
                'id': product['id'],
                'title': product['title'],
                'price': product['price'],
                'description': product['description'],
                'img': main_img
            }
            data.append(obj)
        data[-1]['last_product'] = True

        return JsonResponse({'data': data})


class LoginView(views.View):
    def get(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'login.html', context)


class RegistrationView(views.View):

    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        context = {
            'form': form
        }
        return render(request, 'registration.html', context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.email = form.cleaned_data['email']
            new_user.first_name = form.cleaned_data['first_name']
            new_user.last_name = form.cleaned_data['last_name']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            Customer.objects.create(
                user=new_user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address']
            )
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            login(request,user)
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'registration.html', context)











# class ChangeSpecification(View):
#     def post(self, request, *args, **kwargs):
#         print(request.POST)
#         return HttpResponseRedirect('/cart/')
#
#
# class AddToCartView(View):
#     def get(self, request, *args, **kwargs):
#         customer = Customer.objects.get(user=request.user)
#         cart = Cart.objects.get(owner=customer, in_order=False)
#         product = Product.objects.get(slug=kwargs.get('product_slug'))
#
#         cart_product, created = CartProduct.objects.get_or_create(
#             user=cart.owner, product=product, final_price=product.price, qty=1
#         )
#         if(created):
#             cart.products.add(cart_product)
#
#         cart.save()
#         return HttpResponseRedirect('/cart/')
#
#
# class DeleteFromCart(View):
#     def get(self, request, *args, **kwargs):
#         customer = Customer.objects.get(user=request.user)
#         cart = Cart.objects.get(owner=customer, in_order=False)
#
#         product = Product.objects.get(slug=kwargs.get('product_slug'))
#
#         cart_product = CartProduct.objects.get(
#             user=cart.owner, product=product,
#         )
#         cart.products.remove(cart_product)
#         cart_product.delete()
#         cart.save()
#         return HttpResponseRedirect('/cart/')
#
#
# class CartView(View):
#     def get(self, request, *args, **kwargs):
#         customer = Customer.objects.get(user=request.user)
#         cart = Cart.objects.get(owner=customer)
#         products = CartProduct.objects.filter(user=customer)
#         images = []
#         for product in products:
#             images.append(get_object_or_404(ImageGallery, object_id=product.product.id, is_main=True))
#         context = {
#             'cart': cart,
#             'images': images,
#         }
#         return render(request, 'cart.html', context)