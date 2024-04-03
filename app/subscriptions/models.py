from django.db import models
from common.models import CommonModel
from users.models import User


class SubscriptionManager(models.Manager):
    def get_subscriber_count(self, user_id):
        return Subscription.objects.filter(subscribed_to=user_id).count()


class Subscription(CommonModel):
    subscriber = models.ForeignKey(
        User,
        related_name='subscriptions',
        on_delete=models.CASCADE
    )
    subscribed_to = models.ForeignKey(
        User,
        related_name='subscribers',
        on_delete=models.CASCADE
    )
