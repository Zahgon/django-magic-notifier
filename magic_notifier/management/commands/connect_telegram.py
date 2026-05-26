from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from magic_notifier.telegram_clients.telethon import TelethonClient
from django.conf import settings

User = get_user_model()


class Command(BaseCommand):
    """The command `test_email_template` is used to test a template email.
    This is very useful in development."""


