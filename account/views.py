from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .serializers import RegisterUserSerializer

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
