from rest_framework import serializers
from .models import CustomUser
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate




class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'firstname', 'lastname', 'phonenumber', 'gender', 'dateofbirth', 
            'location', 'profilepic','role','password', 'is_blocked']
    def validate_password(self, value):
        if not value:
            raise serializers.ValidationError("Password is required.")
        # You can add more password validation logic here if needed.
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = CustomUser(**validated_data)
        user.password = make_password(password)  # Ensure the password is hashed
        user.save()
        return user
    


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(email=data['email'], password=data['password'])
        if user is None:
            raise serializers.ValidationError('Invalid credentials')
        return {'user': user}
    


class UpdateProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['firstname', 'lastname', 'phonenumber', 'location', 'profilepic']




class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect")
        return value




class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'username', 'role'] 


