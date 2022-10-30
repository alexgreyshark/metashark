import json
import os

from django.core.management.base import BaseCommand
from users.models import User


def generate_superuser():
    """Заполнение суперадминистратором
    """
    filepath = os.path.abspath(os.path.dirname(__file__))
    file = open(f'{filepath}/superuser.json', 'r')
    data = json.load(file)
    for user in data:
        check_exists = User.objects.filter(username=user['username']).exists()
        if check_exists:
            print(f"{user['username']} уже есть")
        else:
            User.objects.create_superuser(
                **user,
            )
    file.close()


class Command(BaseCommand):

    def handle(self, *args, **options):
        generate_superuser()
