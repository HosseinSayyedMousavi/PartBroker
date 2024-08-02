from rest_framework import serializers
from django.core import exceptions
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from .models import User 

class RegistrationSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(max_length = 255 , write_only = True)
    class Meta:
        model = User
        fields = ["phone_number","password","password1"]

    def validate(self,attrs):
        if attrs.get('password') != attrs.get('password1'):
            raise serializers.ValidationError({"detail" : _("passwords does\'nt match")})
        try:
             validate_password(attrs.get('password'))
        except exceptions.ValidationError as e:
             raise serializers.ValidationError({"password":list(e.messages)})
        
        return super().validate(attrs)

    def create(self,validated_data):
        validated_data.pop('password1',None)
        return User.objects.create_user(**validated_data)


class UpdateUserAPIViewSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(max_length=20,required=False)
    last_name = serializers.CharField(max_length=20,required=False)


class UserAPIViewSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    first_name = serializers.CharField(max_length=20,required=False)
    last_name = serializers.CharField(max_length=20,required=False)
    phone_number = serializers.CharField(max_length=11,required=False)
    created_date = serializers.DateTimeField(required = False)
    updated_date = serializers.DateTimeField(required = False)

