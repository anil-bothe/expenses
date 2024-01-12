from django.db import models
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token


"""your models"""
from app.model.roles import Roles
from app.model.users import User
from app.model.expense import Expense
from app.model.balance import Balance


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
