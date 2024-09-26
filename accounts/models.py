from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
    phone_number = models.CharField(
        max_length=8,
        validators=[RegexValidator(
            r'^\d{8}$', 'Ingrese un número de teléfono válido de 8 dígitos.')],
        unique=True
    )
    address = models.TextField()
    delivery_instructions = models.TextField(blank=True)
    contact_person_phone = models.CharField(
        max_length=8,
        validators=[RegexValidator(
            r'^\d{8}$', 'Ingrese un número de teléfono válido de 8 dígitos.')],
    )
    is_owner = models.BooleanField(default=False)
    is_manager = models.BooleanField(default=False)

    # Modificar las relaciones many-to-many para usar related_name personalizado
    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='custom_user_set',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='user',
    )

    def __str__(self):
        return self.username
