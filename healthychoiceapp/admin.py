from django.contrib import admin
from .models import Category, Product, Recipe, Article, Favourite

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category',)

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('pub_date', 'name')


admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Recipe)
admin.site.register(Article)
admin.site.register(Favourite)
