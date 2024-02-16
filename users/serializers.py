from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from users.models import DeveloperProfile
from users.validators import (
    validate_password_digit,
    validate_password_uppercase,
    validate_password_lowercase,
    validate_password_symbol,
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """
    User serializers
    creating new clients
    """

    id = serializers.CharField(
        read_only=True,
    )

    username = serializers.CharField(
        max_length=20,
        min_length=4,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(
        max_length=128,
        min_length=5,
        write_only=True,
        validators=[
            validate_password_digit,
            validate_password_uppercase,
            validate_password_symbol,
            validate_password_lowercase,
        ],
    )

    class Meta:
        model = User
        fields = (
            "id",
            "firstname",
            "lastname",
            "email",
            "username",
            "password",
            "image",
            "about",
            "is_verified",
            "is_client",
            "is_admin",
            "is_user",
            "is_developer",
        )

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_client = True
        user.save()
        return user


class DeveloperSerializer(serializers.ModelSerializer):
    """
    Developer Serializer
    Creating developer account
    Verified on creation
    """

    id = serializers.CharField(
        read_only=True,
    )

    username = serializers.CharField(
        max_length=20,
        min_length=4,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )

    password = serializers.CharField(
        max_length=128,
        min_length=5,
        write_only=True,
        validators=[
            validate_password_digit,
            validate_password_uppercase,
            validate_password_symbol,
            validate_password_lowercase,
        ],
    )

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "password",
            "is_verified",
            "is_client",
            "is_admin",
            "is_user",
            "is_developer",
        )

    def create(self, validated_data):
        developer = User.objects.create_user(**validated_data)
        developer.is_developer = True
        developer.save()
        DeveloperProfile.objects.create(developer=developer)
        return developer


class DeveloperProfileSerializer(serializers.ModelSerializer):
    """
    Dveloper profile serializer
    """

    developer = serializers.CharField(read_only=True, source="developer.username")
    resume = serializers.FileField(use_url=True, required=False)
    status = serializers.CharField(min_length=2, allow_blank=True, required=False)
    skills = serializers.CharField(min_length=1, allow_blank=True, required=False)

    class Meta:
        model = DeveloperProfile
        fields = (
            "developer",
            "resume",
            "status",
            "skills",
        )

    def update(self, instance, validated_data):
        instance.resume = validated_data.get("resume", instance.resume)
        instance.status = validated_data.get("status", instance.status)
        instance.skills = validated_data.get("skills", instance.skills)
        instance.save()
        return instance


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):  # type:ignore[no-untyped-def]
        self.token = attrs["refresh"]
        return attrs

    def save(self, **kwargs):  # type:ignore[no-untyped-def]
        try:
            RefreshToken(self.token).blacklist()

        except TokenError:
            raise serializers.ValidationError(
                "Invalid or expired token", code="invalid_token"
            )
