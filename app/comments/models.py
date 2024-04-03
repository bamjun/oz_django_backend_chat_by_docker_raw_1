from django.db import models
from common.models import CommonModel
from users.models import User
from videos.models import Video


class Comment(CommonModel):
    like = models.PositiveIntegerField(default=0)
    dislike = models.PositiveIntegerField(default=0)
    content = models.TextField(max_length=500)

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)

    def to_dict(self):
        return {
            'email': self.user.email,
            'nickname': self.user.nickname,
            'content': self.content,
            'like': self.like,
            'dislike': self.dislike,
        }
