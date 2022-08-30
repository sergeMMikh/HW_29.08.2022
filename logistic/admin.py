from django.contrib import admin

from .models import Product, StockProduct, Stock

@admin.register(Product)
class ArticleAdmin(admin.ModelAdmin):
    ...

@admin.register(StockProduct)
class ArticleAdmin(admin.ModelAdmin):
    ...

@admin.register(Stock)
class ArticleAdmin(admin.ModelAdmin):
    ...
