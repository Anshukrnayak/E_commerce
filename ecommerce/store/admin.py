from django.contrib import admin
from .models import Category_model,Product_model


@admin.register(Category_model)
class CategoryAdmin(admin.ModelAdmin):
    list_display=['title','slug']



@admin.register(Product_model)
class Product_Admin(admin.ModelAdmin):
    list=['user','title','slug','category','price']

    