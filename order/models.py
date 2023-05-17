from django.db import models
from account.models import User
from main.models import Product

# Create your models here.

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def total_price(self):
        items = self.items.all()
        # в данном случае мы ссылаемся на related_name='items', так как поля order
        # не существует, мы лишь ссылаемся на него. Благоларя related_name мы как раз можем сслыалатьс на него
        if items.exists():
            return sum([item.product.price * item.quantity for item in items])
        return 0


class OrderItems(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    quantity = models.PositiveIntegerField(default=1)

