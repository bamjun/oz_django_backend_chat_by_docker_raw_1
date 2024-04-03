# from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from .models import Video
from users.serializers import UserSerializer
from comments.serializers import CommentSerializer
from rest_framework import serializers
from reactions.models import Reaction
 
class VideoSerializer(ModelSerializer):

    user = UserSerializer(read_only=True)
    comment_set = CommentSerializer(read_only=True, many=True)
    # 부모가 자녀를 찾기 위해서 필요한 개념: Reverse Accessor

    # likes_count = serializers.IntegerField(read_only=True)
    # dislikes_count = serializers.IntegerField(read_only=True)
    reations = serializers.SerializerMethodField()

    class Meta:
        model = Video
        fields = '__all__'  # Video모델의 전체 필드를 보여줘

    def get_reations(self, video):
        return Reaction.get_video_reaction(video=video)