from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView
from django.views import View
from django import views
from .models import *
from django.http import JsonResponse



class BaseView(views.View):
    def get(self, request, *args, **kwargs):
        return render(request, 'base.html', {})



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
    def get(self,request, *args, **kwargs):
        last_product_id = request.GET.get('lastProductId')
        more_products = Product.objects.filter(pk__gt=int(last_product_id)).values('id', 'title', 'price', 'description')[:9]
        images = ImageGallery.objects.filter(object_id=last_product_id, is_main = True)

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

    class LoginUser(DataMixin)