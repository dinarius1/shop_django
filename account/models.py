from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from .utils import send_activation_code

# Create your models here.
class UserManager(BaseUserManager):
    use_in_magrations = True #нужен,чтобы менеджер нормально роботал, и чтобы мог обновляться.
    #Также в дальнейшем большая вероятность,что мы будем расширять наш менеджер

    def create_user(self, email, password, phone, **kwargs):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        #normalize_email - он по факту приводит нашу почту в нормальный формат
        user = self.model(email=email, phone=phone, **kwargs)
        #self.model = User - это ожно и тоже, но нужно написать так,
        # так как наш класс User написан ниже класса Менеджера
        user.set_password(password) #хеширование пароля
        user.create_activation_code()  # генерируем активац. код
        send_activation_code(user.email, user.activation_code) #отправляем на почту
        user.save(using=self._db) #сохраняет наши данные в бд, а именно self._db,
        # поэтому нужно добавлять using
        Billing.objects.create(user=user) #так как эта функция, то она работает только тогда, когда мы ее вызовем
        return user

    def create_superuser(self, email, password, phone, **kwargs):
        if not email:
            raise ValueError('Email is required')
        kwargs['is_staff'] = True #даем права суперадмина
        #kwargs - в виде словаря хотим показать это
        kwargs['is_superuser'] = True
        kwargs['is_active'] = True #не нужно в таком случае подтверждения по почте
        email = self.normalize_email(email)
        #normalize_email - он по факту приводит нашу почту в нормальный формат
        user = self.model(email=email, phone=phone, **kwargs)
        #self.model = User - это ожно и тоже, но нужно написать так,
        # так как наш класс User написан ниже класса Менеджера
        user.set_password(password) #хеширование пароля
        user.save(using=self._db) #сохраняет наши данные в бд, а именно self._db,
        # поэтому нужно добавлять using
        return user
class User(AbstractUser):
    username = None #из полей убираем поле username
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=50)
    bio = models.TextField()
    is_active = models.BooleanField(default=False)
    #is_active - отвечает активный пользователь или нет, может ли он что тот делать или нет
    activation_code = models.CharField(max_length=8, blank=True)


    USERNAME_FIELD = 'email'
    #показывает, что через это поля он будет регистрировать пользователя
    REQUIRED_FIELDS = ['phone',]

    objects = UserManager() #указываем нового менеджера

    def create_activation_code(self):  #self - это объект от модельки User, то есть это какоцто пользователь
        from django.utils.crypto import get_random_string
        code = get_random_string(length=8)
        self.activation_code = code
        self.save()


class Billing(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='billing')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def top_up(self, amount):
        """Пополнение счета. Если транзакция прошла успешна, вернется True"""
        if amount > 0:
            self.amount += amount
            self.save()
            return True
        return  False

    def withdraw(self, amount):
        """Снятие со счета. Если транзакция прошла успешна, вернется True"""
        if self.amount >= amount:
            self.amount -= amount
            return True
        return False

