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
    created_at = models.DateTimeField(auto_now_add=True)


    @property
    def average_rating(self):
        ratings = self.ratings.all() #так как ratings связан с продуктом через fk, то можем ссылаться на их related name
        if ratings.exists():
            return sum([x.value for x in ratings]) // ratings.count()
            #ищем среднее значение рейтинга
        return 0



