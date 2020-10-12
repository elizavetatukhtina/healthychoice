from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
import slugify


# Model for storing categories from DailyDozen list
class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


# Model for a card of a product
class Product(models.Model):
    name = models.CharField(max_length=50)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    description = models.TextField()
    image = models.ImageField(upload_to='facts_img/', blank=False)
    slug = models.SlugField(max_length=50, editable=False)
    create_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


def slug_save(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify.slugify(instance.name)


pre_save.connect(slug_save, sender=Product)


# Model for a recipe
class Recipe(models.Model):
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=50, editable=False)
    ingredients = models.ManyToManyField(Product)
    categories = models.ManyToManyField(Category)
    recipe = RichTextUploadingField()
    image = models.ImageField()
    create_time = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name


pre_save.connect(slug_save, sender=Recipe)


# Model for article
class Article(models.Model):
    pub_date = models.DateField()
    name = models.CharField(max_length=200)
    content = RichTextUploadingField()
    slug = models.SlugField(max_length=50, editable=False)
    create_time = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.name


pre_save.connect(slug_save, sender=Article)


class ShoppingList(models.Model):
    content = RichTextField()
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Favourite(models.Model):
    products = models.ManyToManyField(Product)
    recipes = models.ManyToManyField(Recipe)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
