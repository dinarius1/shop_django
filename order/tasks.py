from django.core.mail import send_mail
from .models import Order
from celery import shared_task

@shared_task
def send_successful_payment_message(email : str, total_price : float, items : list):
    # new_line = '\n'
    # {f'{new_line}'.join([item.product.title for item in order.items])}
    # #Или можно так в Продукты:
    message = f"""
Заказ успешно оплачен!

Детали заказа:
Цена: {total_price}
Продукты: 
"""

    for item in items:
        message += f'{item["title"]} ({item["quantity"]})\n'

    send_mail(
        subject='Успешный платёж',
        message=message,
        from_email='a@gmail.com',
        recipient_list=[email]
    )

def send_error_payment_message(email : str, order : Order):
    message = f"""
    Заказ не был оплачен!

    Детали заказа:
    Цена: {order.total_price}
    Продукты: 
    """

    for item in order.items.all():
        message += f'{item.product.title} ({item.quantity})\n'

    send_mail(
        subject='Ошибка оплаты',
        message=message,
        from_email='a@gmail.com',
        recipient_list=[email]
    )
