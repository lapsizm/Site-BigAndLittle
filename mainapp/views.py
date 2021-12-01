from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.views import View
from django import views
from django.db import transaction

from .models import *
from django.http import JsonResponse, HttpResponseRedirect
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib import messages

from .mixins import CartMixin, CreateNotAuthCart


class BaseView(CartMixin, views.View):
    def get(self, request, *args, **kwargs):
        context = {
            'cart': self.cart
        }
        return render(request, 'base.html', context)


class ProductList(CartMixin, views.View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        products = Product.objects.all()[:9]
        images = ImageGallery.objects.filter(is_main=True)
        cart = self.cart
        return render(request, 'catalog.html', locals())


class CategoryDetail(CartMixin, views.View):
    def get(self, request, *args, **kwargs):
        categories = Category.objects.all()
        category = get_object_or_404(Category, slug=kwargs.get('category_slug'))
        products = Product.objects.filter(category__slug=kwargs.get('category_slug'))
        images = []
        for product in products:
            images.append(get_object_or_404(ImageGallery, is_main=True, object_id=product.id))
        cart = self.cart
        return render(request, 'category_detail.html', locals())


class ProductDetail(CartMixin, views.View):
    def get(self, request, *args, **kwargs):
        category = get_object_or_404(Category, slug=kwargs.get('category_slug'))
        product = get_object_or_404(Product, slug=kwargs.get('product_slug'))
        images = ImageGallery.objects.filter(object_id=product.id)
        colors = ColorField.objects.filter(object_id=product.id)
        sizes = SizeField.objects.filter(object_id=product.id)
        cart = self.cart
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


class LoginView(CartMixin, views.View):
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
                if request.session['cart_id']:
                    CreateNotAuthCart(request)
                return HttpResponseRedirect('/')
        context = {
            'form': form,
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
            login(request, user)
            if request.session['cart_id']:
                CreateNotAuthCart(request)
            return HttpResponseRedirect('/')
        context = {
            'form': form
        }
        return render(request, 'registration.html', context)


class AccountView(CartMixin, views.View):
    def get(self, request, *args, **kwargs):
        customer = Customer.objects.get(user=request.user)
        context = {
            'customer': customer,
            'cart': self.cart
        }
        return render(request, 'personal_area.html', context)


class PersonalData(views.View):
    pass


class CartView(views.View):
    pass


class HistoryOrders(views.View):
    pass


class AddToCartView(CartMixin, views.View):
    def post(self, request, *args, **kwargs):
        product = Product.objects.get(slug=kwargs.get('product_slug'))
        color = request.POST.get('color')
        size = request.POST.get('size')
        color_field = ColorField.objects.filter(color=color, object_id=product.id).first()
        size_field = SizeField.objects.filter(size=size, object_id=product.id).first()
        data = {
            'cart': self.cart,
            'product': product,
            'size': size_field,
            'color': color_field
        }
        if request.user.is_authenticated:
            data.update({'user': self.cart.owner})
            cart_product, created = CartProduct.objects.get_or_create(**data)

        else:
            data.update({'session_key': request.session.session_key})
            cart_product, created = CartProduct.objects.get_or_create(**data)

        if created:
            cart_product.recalc_product()
            self.cart.products.add(cart_product)
            self.cart.recalc()
            messages.add_message(request, messages.INFO, "Товар успешно добавлен")
            self.cart.save()
        else:
            messages.add_message(request, messages.INFO, "Товар уже добавлен в корзину")

        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class DeleteFromCart(CartMixin, View):
    def get(self, request, *args, **kwargs):
        product = Product.objects.get(slug=kwargs.get('product_slug'))
        qty = kwargs.get('qty')
        color = kwargs.get('color')
        size = kwargs.get('size')
        color_field = ColorField.objects.filter(color=color, object_id=product.id).first()
        size_field = SizeField.objects.filter(size=size, object_id=product.id).first()
        # final_price = product.price * qty
        data = {
            'cart': self.cart,
            'product': product,
            'size': size_field,
            'color': color_field
        }
        if request.user.is_authenticated:
            data.update({'user': self.cart.owner})
            cart_product, created = CartProduct.objects.get_or_create(**data)

        else:
            data.update({'session_key': request.session.session_key})
            cart_product, created = CartProduct.objects.get_or_create(**data)

        self.cart.products.remove(cart_product)
        self.cart.recalc()
        cart_product.delete()
        messages.add_message(request, messages.INFO, "Товар успешно удален")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class ChangeQTY(CartMixin, views.View):
    def post(self, request, *args, **kwargs):
        product = Product.objects.get(slug=kwargs.get('product_slug'))
        color = kwargs.get('color')
        size = kwargs.get('size')
        color_field = ColorField.objects.filter(color=color, object_id=product.id).first()
        size_field = SizeField.objects.filter(size=size, object_id=product.id).first()

        data = {
            'cart': self.cart,
            'product': product,
            'size': size_field,
            'color': color_field
        }
        if request.user.is_authenticated:
            data.update({'user': self.cart.owner})
            cart_product, created = CartProduct.objects.get_or_create(**data)

        else:
            data.update({'session_key': request.session.session_key})
            cart_product, created = CartProduct.objects.get_or_create(**data)

        qty = int(request.POST.get('qty'))
        cart_product.qty = qty
        cart_product.recalc_product()
        self.cart.recalc()
        messages.add_message(request, messages.INFO, "Кол-во успешно изменено")
        return HttpResponseRedirect(request.META['HTTP_REFERER'])


class CartView(CartMixin, views.View):
    def get(self, request, *args, **kwargs):
        products = CartProduct.objects.filter(user=self.cart.owner)
        images = []
        for product in products:
            image = get_object_or_404(ImageGallery, object_id=product.product.id, is_main=True)
            if not image in images:
                images.append(image)

        context = {
            'cart': self.cart,
            'images': images,
        }
        return render(request, 'cart.html', context)


class CheckoutView(CartMixin, views.View):
    def get(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        context = {
            'cart': self.cart,
            'form': form,
        }
        return render(request, 'checkout.html', context)


class MakeOrderView(CartMixin, views.View):
    # for save transactions
    @transaction.atomic()
    def post(self, request, *args, **kwargs):
        form = OrderForm(request.POST or None)
        customer = Customer.objects.get(user=request.user)
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.customer = customer
            new_order.first_name = form.cleaned_data['first_name']
            new_order.second_name = form.cleaned_data['second_name']
            new_order.last_name = form.cleaned_data['last_name']
            new_order.phone = form.cleaned_data['phone']
            new_order.address = form.cleaned_data['address']
            new_order.comment = form.cleaned_data['comment']
            new_order.save()

            self.cart.in_order = True
            self.cart.save()
            new_order.cart = self.cart
            new_order.save()
            customer.customer_orders.add(new_order)

            messages.add_message(request, messages.INFO, 'Спасибо за заказ. Менеджр с вами свяжется!')
            return HttpResponseRedirect('/')
        return HttpResponseRedirect('/checkout/')
