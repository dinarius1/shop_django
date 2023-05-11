from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
#redirect -перенапрявляет наш запрос на какую то ссылку в браузере!!!!

from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .serializers import RegisterUserSerializer
from .models import User

# Create your views here.

class RegisterUserView(APIView):
    @swagger_auto_schema(request_body=RegisterUserSerializer())
    def post(self,request):
        serializer = RegisterUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) 
        #вырабатываются все функции, которые мы прописали в сериализаторe, связанные с validate
        serializer.save()   
        #при сейве вырабатывается def create(self, validated_data) из сериализатора
        return Response('Вы успешно зарегистрировались', status=201)

class ActivateView(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        #1 activation_code - это поля в модельке
        #2 activation_code - это параметр из метода
        user.is_active = True
        user.activation_code = ''
        user.save() #сохраняем на уровне бд
        return redirect('https://google.com')


