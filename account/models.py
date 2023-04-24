from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager

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
        user.save(using=self._db) #сохраняет наши данные в бд, а именно self._db,
        # поэтому нужно добавлять using
        return user

    def create_superuser(self, email, password, phone, **kwargs):
        if not email:
            raise ValueError('Email is required')
        kwargs['is_staff'] = True #даем права суперадмина
        #kwargs - в виде словаря хотим показать это
        kwargs['is_superuser'] = True
        kwargs['is_activate'] = True
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

    USERNAME_FIELD = 'email'
    #показывает, что через это поля он будет регистрировать пользователя
    REQUIRED_FIELDS = ['phone',]

    objects = UserManager() #указываем нового менеджера

