from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from users.models import DeveloperProfile
from users.validators import (
    validate_password_digit,
    validate_password_uppercase,
    validate_password_lowercase,
    validate_password_symbol,
)
from users.token import account_activation_token
from hireadeveloper.settings.base import EMAIL_USER, DOMAIN

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
    image = serializers.FileField(use_url=True, required=False)

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

    @staticmethod
    def send_activation_email(user, request):
        """
        send verification email
        """
        current_site = get_current_site(request)
        email_body = render_to_string(
            "email_verification.html",
            {
                "user": user,
                "domain": DOMAIN,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )

        send_mail(
            "Activate your account",
            email_body,
            EMAIL_USER,
            [user.email],
            fail_silently=False,
        )

    def create(self, validated_data):
        request = self.context.get("request")
        user = User.objects.create_user(**validated_data)
        user.is_client = True
        user.save()
        self.send_activation_email(user, request)
        return user


class VerifyEmailSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    class Meta:
        fields = ("uidb64", "token")

    def validate(self, data):
        user = None
        try:
            user_id = force_str(urlsafe_base64_decode(data.get("uidb64")))
            user = User.objects.get(id=user_id)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid user id", code="invalid_code")

        token = data.get("token")
        if user and not account_activation_token.check_token(user, token):
            raise serializers.ValidationError("Invalid token", code="invalid_token")

        return data

    def save(self, **kwargs):
        user_id = force_str(urlsafe_base64_decode(self.validated_data.get("uidb64")))
        user = User.objects.get(id=user_id)
        user.is_verified = True
        user.save()
        return user


class DeveloperSerializer(serializers.ModelSerializer):
    """
    Developer Serializer
    Creating developer account
    Verified on creation
    """

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
            "firstname",
            "lastname",
            "username",
            "password",
            "created_at",
            "is_verified",
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
    role = serializers.CharField(min_length=2, allow_blank=True, required=False)
    skills = serializers.CharField(min_length=1, allow_blank=True, required=False)
    github = serializers.URLField(allow_blank=True, required=False)
    instagram = serializers.URLField(allow_blank=True, required=False)
    twitter = serializers.URLField(allow_blank=True, required=False)
    linkedin = serializers.URLField(allow_blank=True, required=False)
    website = serializers.URLField(allow_blank=True, required=False)

    class Meta:
        model = DeveloperProfile
        fields = (
            "developer",
            "resume",
            "role",
            "skills",
            "github",
            "twitter",
            "linkedin",
            "instagram",
            "website",
        )

    def update(self, instance, validated_data):
        instance.resume = validated_data.get("resume", instance.resume)
        instance.role = validated_data.get("role", instance.role)
        instance.skills = validated_data.get("skills", instance.skills)
        instance.github = validated_data.get("github", instance.github)
        instance.twitter = validated_data.get("twitter", instance.twitter)
        instance.linkedin = validated_data.get("linkedin", instance.linkedin)
        instance.instagram = validated_data.get("instagram", instance.instagram)
        instance.website = validated_data.get("website", instance.website)
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
