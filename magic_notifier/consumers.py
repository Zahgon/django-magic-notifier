import binascii
import ctypes
import json
import logging
import traceback
from datetime import date, datetime, timedelta
from pathlib import Path

from asgiref.sync import async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import WebsocketConsumer
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from .models import Notification
from .serializers import NotificationSerializer

logger = logging.getLogger("notif")


class PushNotifConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.token: str = None
        self.user = None

    def connect(self):
        from .utils import get_settings, import_attribute

        try:
            logger.info(f"accepting")
            self.accept()

            self.token = self.scope["url_route"]["kwargs"]["token"]
            get_user_from_ws_token_func = import_attribute(get_settings("USER_FROM_WS_TOKEN_FUNCTION"))
            self.user = get_user_from_ws_token_func(self.token)


            async_to_sync(self.channel_layer.group_add)(f"user-{self.user.id}", self.channel_name)

            logger.info("Accepted")
        except Exception as e:
            print(traceback.print_exc())
            logger.error(traceback.format_exc())



    def notify(self, data: dict):
        self.send(json.dumps(data))



