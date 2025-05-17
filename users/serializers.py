from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()

class RegisterUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password1 = serializers.CharField(min_length=8, write_only=True)
    password2 = serializers.CharField(min_length=8, write_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        user = User.objects.filter(email=email)
        if user.exists():
            raise serializers.ValidationError("Этот емейл уже занят!!!")
        password1 = attrs.pop("password1")
        password2 = attrs.pop("password2")
        if not password1 or not password2:
            raise serializers.ValidationError("Оба поля пароля обязательны.")
        if password1 != password2:
            raise serializers.ValidationError("Пароли не совпадают!")
        if len(password1) < 8:
            raise serializers.ValidationError("Пароль должен быть не менее 8 символов.")
        if password1.islower():
            raise serializers.ValidationError("Первый символ должен быть в верхнем регистре!")
        if not any(char in "!@#$%^&*?~" for char in password1):
            raise serializers.ValidationError("Пароль должен содержать хотя бы один специальный символ (!@#$%^&*?~).")
        return attrs


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8, write_only=True)
