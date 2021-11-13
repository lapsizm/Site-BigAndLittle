from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import *


class ImageGalleryInline(GenericTabularInline):
    model = ImageGallery
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


