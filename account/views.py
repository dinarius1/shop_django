from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
#redirect -перенапрявляет наш запрос на какую то ссылку в браузере!!!!

from django.shortcuts import get_object_or_404
from decimal import Decimal, InvalidOperation
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema

from .serializers import RegisterUserSerializer, BillingSerializer
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

class TopUpBillingView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=BillingSerializer())
    def post(self, request):
        #{'amount': 100}
        amount = request.data.get('amount')
        if not amount:
            return Response('Amount is required!', status=400)

        try:
            amount = Decimal(amount)
        except:
            return Response('Invalid amount', status=400)

        billing = request.user.billing
        if billing.top_up(amount):
            return Response(status=200)
        return Response('Invalid amount', status=400)


