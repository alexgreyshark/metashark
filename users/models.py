from dataclasses import dataclass
from django.db import models
from django.contrib.auth.models import AbstractUser


@dataclass
class UserRoles:
    admin: str = '1'
    curator: str = '2'


class User(AbstractUser):
    """Кастомная модель пользователя
    """
    ROLE_CHOICES = (
        (UserRoles.admin, 'Администратор'),
        (UserRoles.curator, 'Куратор'),
    )

    role = models.CharField(
        max_length=1,
        verbose_name='Роль',
        choices=ROLE_CHOICES,
    )
    REQUIRED_FIELDS = [
        'email',
        'role',
    ]
