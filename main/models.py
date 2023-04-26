from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=100)

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name= 'products')
    #если удаляется категория, то удаляется и весь пост
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    #decimal_places - показывает сколько символов после точки
    description = models.TextField()
    quantity = models.IntegerField()
