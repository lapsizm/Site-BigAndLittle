from django.shortcuts import render, get_object_or_404
from django import views
from .models import Category, Product
from django.views.generic import DetailView


class BaseView(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'base.html', {})


class ProductDetailView(DetailView):

    def dispatch(self, request, *args, **kwargs):
        ct_model = kwargs.get('ct_model')
        self.model = ct_model
        self.queryset = Product.objects.all()
        return super().dispatch(request, *args, **kwargs)

    context_object_name = 'product'
    template_name = 'product_detail.html'
    slug_url_kwarg = 'slug'

# def CatalogList(request, category_slug=None):
#     category = None
#     categories = Category.objects.all()
#     products = Product.object.all()
#     if category_slug:
#         category = get_object_or_404(Category, slug=category_slug)
#         products = products.filter(category=category)
#     return render(request, 'catalog.html', {
#         'category': category,
#         'categories': categories,
#         'products': products,
#     })
#
#
# def ProductDetail(request, id, slug):
#     product = get_object_or_404(Product, id=id, slug=slug)
#     return render(request, 'product_detail.html', {'product': product})
