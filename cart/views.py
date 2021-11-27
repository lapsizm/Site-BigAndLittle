from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from mainapp.models import Product, ImageGallery
from .cart import Cart


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    size = request.POST.get('size')
    color = request.POST.get('color')

    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product,
             color=color,
             size=size)
    return redirect('cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart_detail')


def cart_detail(request):
    cart = Cart(request)
    images = []
    for item in cart.cart.keys():
        images.append(get_object_or_404(ImageGallery, object_id=item, is_main=True))
    return render(request, 'cart/detail.html', locals())
