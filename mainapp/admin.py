from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models import *

class ImageGalleryInline(GenericTabularInline):
    model = ImageGallery
    readonly_fields = ('image_url',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ImageGalleryInline]


admin.site.register(Category)
admin.site.register(ImageGallery)

