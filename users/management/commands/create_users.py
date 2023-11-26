import json

from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        """Загружает из файла данные и создает пользователей"""
        with open('users/fixtures/users.json') as file:
            data = json.load(file)
            for obj in data:
                user = User.objects.create(
                        email=obj['fields']['email'],
                        is_staff=obj['fields']['is_staff'],
                        is_superuser=obj['fields']['is_superuser'],
                        country=obj['fields']['country'],
                        phone=obj['fields']['phone'],
                        avatar=obj['fields']['avatar']

                )
                user.set_password(obj['fields']['password'])
                user.save()
