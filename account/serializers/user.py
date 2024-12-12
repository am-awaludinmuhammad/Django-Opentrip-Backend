import re
from account.models import User
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_confirm = serializers.CharField(write_only=True)
    name = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')

        # set fields optional for patch
        if request and request.method in ['PATCH']:
            self.fields['password'].required = False
            self.fields['password_confirm'].required = False

    class Meta:
        model = User
        fields = ('id', 'email','name','phone','avatar','is_active','password', 'password_confirm')

    def validate_phone(self, value):
        if value and not re.match(r'^62\d{8,15}$', value):
            raise serializers.ValidationError("Invalid phone number. It must start with '62' and contain between 8 and 15 digits.")
        return value

    def validate(self, data):
        password = data.get('password', None)
        password_confirm = data.get('password_confirm', None)
        email = data.get('email', None)
        request = self.context.get('request')
        
        if password and password != password_confirm:
            raise serializers.ValidationError({"password": ["Password confirmation does not match."]})
        
        if email and request.method == 'POST' and User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({"email": ["Email address is already taken."]})

        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)