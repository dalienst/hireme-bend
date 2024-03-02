from django.db import models
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from cloudinary.models import CloudinaryField
from users.abstracts import TimeStampedModel, UniversalIdModel, AbstractProfile


class UserManager(BaseUserManager):
    use_in_migrations: True

    def _create_user(self, username: str, email: str, password: str, **kwargs):
        """
        Create and save a user with the given username, email, and password.
        """
        if not username:
            raise ValueError("The given username must be set")
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, username: str, email: str, password: str, **kwargs):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        return self._create_user(username, email, password, **kwargs)

    # def create_developer(self, username: str, email: str, password: str, **kwargs):
    #     kwargs.setdefault("is_staff", False)
    #     kwargs.setdefault("is_superuser", False)
    #     kwargs.setdefault("is_client", False)
    #     kwargs.setdefault("is_admin", False)
    #     kwargs.setdefault("is_developer", True)
    #     return self._create_developer(username, email, password, **kwargs)

    def create_superuser(self, username: str, email: str, password: str, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_client", True)
        kwargs.setdefault("is_admin", True)
        kwargs.setdefault("is_developer", True)

        if not password:
            raise ValueError("Password is required")
        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if kwargs.get("is_client") is not True:
            raise ValueError("Superuser must have is_client=True")
        if kwargs.get("is_admin") is not True:
            raise ValueError("Superuser must have is_admin=True")
        if kwargs.get("is_developer") is not True:
            raise ValueError("Superuser must have is_developer=True")

        return self._create_user(username, email, password, **kwargs)


class User(
    AbstractBaseUser,
    PermissionsMixin,
    TimeStampedModel,
    UniversalIdModel,
    AbstractProfile,
):
    """
    Users Model:
    - Admin
    - Employee
    - Clients
    """

    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
    )
    email = models.EmailField(
        unique=True,
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_verified = models.BooleanField(default=False)
    is_client = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_user = models.BooleanField(default=True)
    is_developer = models.BooleanField(default=False)

    objects = UserManager()
    REQUIRED_FIELDS = ["username", "password"]
    USERNAME_FIELD = "email"

    class Meta:
        ordering = [
            "-created_at",
        ]

    def __str__(self) -> str:
        return self.username


class DeveloperProfile(UniversalIdModel):
    """
    Developers Model:
    add resume
    add status
    add professional skills
    """

    developer = models.OneToOneField(User, on_delete=models.CASCADE)
    resume = CloudinaryField("resume", null=True, blank=True)
    skills = models.TextField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)

    DEVELOPER_ROLE = (
        ("SD", "Software Developer"),
        ("ML", "Machine Learning Engineer"),
        ("SE", "Software Engineer"),
    )

    role = models.CharField(
        max_length=2,
        choices=DEVELOPER_ROLE,
        default="SD",
    )

    def __str__(self) -> str:
        return self.employee.username
