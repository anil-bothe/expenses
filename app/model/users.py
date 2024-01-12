from django.db import models
from django.contrib.auth.models import UserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from app.model.roles import Roles


class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        group, created = Roles.objects.get_or_create(name="Superuser")
        extra_fields.setdefault("role_id", group.id)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


# Customized User
class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(_("name"), max_length=50, null=True)
    email = models.EmailField(_("email address"), unique=True, null=True)
    mobile = models.CharField(_("mobiles"), max_length=16, null=True, blank=True)

    role = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    login_attempt = models.IntegerField(default=0)
    last_ip = models.CharField(max_length=50, null=True, blank=True)

    STATUS_BY = ((0, "inactive"), (1, "active"), (2, "deleted"), (3, "blocked"))
    status = models.IntegerField(choices=STATUS_BY, default=1)

    username = models.CharField(
        _("username"),
        max_length=150,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        null=True,
        blank=True,
        unique=True,
    )
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []


    def __str__(self) -> str:
        return str(self.name)
    
    class Meta:
        db_table = "user"
        verbose_name = _("user")
        verbose_name_plural = _("users")
