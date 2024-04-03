from rest_framework.serializers import ModelSerializer
from .models import Reaction


class ReactionSerializer(ModelSerializer):
    class Meta:
        model = Reaction
        fields = '__all__'
        read_only_fields = ['user', 'video']
