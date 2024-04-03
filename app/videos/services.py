from reactions.models import Reaction
from subscriptions.models import Subscription
from django.shortcuts import get_object_or_404
from .models import Video
from comments.models import Comment


class VideoService():
    def get_like_count(video_id):
        return Reaction.objects.filter(
            video=video_id, reaction=Reaction.LIKE
            ).count()

    def get_dislike_count(video_id):
        return Reaction.objects.filter(
            video=video_id, reaction=Reaction.DISLIKE
            ).count()

    def get_subscriber_count(video_owner):
        return Subscription.objects.filter(
            subscribed_to=video_owner
            ).count()

    def get_is_subscribed(user_id, video_owner):
        return Subscription.objects.filter(
            subscriber=user_id, subscribed_to=video_owner
            ).exists()

    def get_reaction(user_id, video_id):
        return get_object_or_404(
            Reaction, user=user_id, id=video_id
            ).reaction

    def increase_view_count(video_id):
        video = get_object_or_404(Video, id=video_id)
        video.views_count += 1
        video.save()

    def get_comment_count(video_id):
        return Comment.objects.filter(video=video_id).count()

    def get_comment_list(video_id):
        return Comment.objects.filter(video=video_id).order_by('-created_at')
