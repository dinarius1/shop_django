from rest_framework import serializers

from .models import User, Billing

class RegisterUserSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=4, required = True)

    class Meta:
        model = User
        fields = ('email', 'phone', 'password', 'password_confirm')

    def validate(self, attrs): #attrs - содержит в себе словарь с данными формата json 
        # ATTRS -> OrderedDict([('email', 'admin1@gmail.com'), ('phone', '996700071102'), ('password', '12345'), ('password_confirm', '12345')])
        pass1 = attrs.get('password')
        pass2 = attrs.pop('password_confirm')
        # ATTRS AFTER POP -> # ATTRS -> OrderedDict([('email', 'admin1@gmail.com'), ('phone', '996700071102'), ('password', '12345')])
        if pass1 != pass2:
            raise serializers.ValidationError("Passwords do not match")
        return attrs
    
    def validate_email(self, email):
        # EMAIL  {'email': 'admin3@gmail.com'}
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with this email already exists')
        return email
    
    def create(self, validated_data):
        # VALIDATED_DATA -> {'email': 'admin3@gmail.com', 'phone': '996700071102', 'password': '12345'}
        # print(validated_data)
        return User.objects.create_user(**validated_data)



class BillingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Billing
        fields = ('amount',)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'phone', 'bio')

    def to_representation(self, instance: User):
        #self - это обекты от ProfileSerializer
        #instance - это обекты от User. Его получим после того как нам передадут аргумент
        rep = super().to_representation(instance)
        #собирает словарь из fields = ('email', 'phone', 'bio')
        rep['billing'] = instance.billing.amount
        return rep