from user.models import User
from rest_framework import serializers
import re
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class JoinSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_password(self, password):
        REGEX_PASSWORD = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$"
        if not re.search(REGEX_PASSWORD, password):
            raise serializers.ValidationError({"detail":"비밀번호 8자 이상 영문, 숫자, 특수문자 하나 이상씩 포함해 주세요."})
        return password

    def create(self, validated_data):
        user  = super().create(validated_data)
        password = user.password
        user.set_password(password)
        user.save()
        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['user_id'] = user.id

        return token