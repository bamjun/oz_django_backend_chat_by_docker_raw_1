from django.db import models
from common.models import CommonModel
from users.models import User
from django.db import models


# class VideoManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().annotate(
#             likes_count=models.Count('reaction', filter=models.Q(reaction__reaction=1)),
#             dislikes_count=models.Count('reaction', filter=models.Q(reaction__reaction=-1)),
#         )


class Video(CommonModel):
    CATEGORY_CHOICES = [
        ('music', 'Music'),
        ('sports', 'Sports'),
        ('entertainment', 'Entertainment'),
        ('education', 'Education'),
        ('game', 'Game'),
        ('movie', 'Movie'),
        ('news', 'News'),
        ('other', 'Other'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500, blank=True)
    category = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    views_count = models.PositiveIntegerField(default=0)
    thumbnail = models.URLField()  # S3에 업로드후 사용할거기 때문에 URL필드 사용
    link = models.URLField()
    video_uploaded_url = models.URLField()
    video_file = models.FileField(upload_to='storage/')

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # objects = VideoManager()

    def to_dict(self):
        return {
            'title': self.title,
            'category': self.category,
            'views_count': self.views_count,
            'description': self.description,
        }
