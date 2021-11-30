from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import *
from django.contrib.sessions.models import Session
class ImageGalleryInline(GenericTabularInline):
    model = ImageGallery
    max_num = 5
    readonly_fields = ('image_url',)


class ColorInline(GenericTabularInline):
    model = ColorField
    extra = 0


class SizeInline(GenericTabularInline):
    model = SizeField
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageGalleryInline, ColorInline, SizeInline]


admin.site.register(Category)
admin.site.register(SizeField)
admin.site.register(ColorField)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Notification)
admin.site.register(Session)




