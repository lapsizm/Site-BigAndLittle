from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView

from django import views
from .models import Category, Product


class BaseView(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'base.html', {})


def ProductList(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    return render(request, 'catalog.html', {'categories': categories, 'products': products})


def CategoryDetail(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category__slug=category_slug)
    return render(request, 'category_detail.html', {'category': category, 'products': products})

def ProductDetail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(Product, slug=product_slug)
    return render(request, 'product_detail.html', {'category': category, 'product': product})

