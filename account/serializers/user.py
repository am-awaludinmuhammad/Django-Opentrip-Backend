from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from account.models import User

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    name = serializers.CharField(required=True)
    
    class Meta:
        model = User
        fields = ('id', 'email','name','phone','avatar','is_active','password', 'password_confirm')

    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError('Password confirmation does not match.')
        
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError('Email address is already taken.')

        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)