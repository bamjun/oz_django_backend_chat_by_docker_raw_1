from django.db import models
from common.models import CommonModel
from users.models import User


class ChatRoom(CommonModel):
    roomname = models.CharField(max_length=100)
    member = models.ManyToManyField(User, through='ChatRoomConnector')


class ChatRoomConnector(CommonModel):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)


class Message(CommonModel):
    message = models.TextField(max_length=500)
    sender = models.ForeignKey(User, on_delete=models.CASCADE)
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
