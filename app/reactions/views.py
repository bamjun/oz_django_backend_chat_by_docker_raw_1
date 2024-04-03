from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Reaction
from videos.models import Video
from rest_framework import status
from django.shortcuts import get_object_or_404
from .serializers import ReactionSerializer


class ReactionDetail(APIView):
    def post(self, request, video_id):
        user_data = request.data
        try:
            serializer = ReactionSerializer(data=user_data)

            if serializer.is_valid(raise_exception=True):
                reaction_obj, created = Reaction.objects.get_or_create(
                    user=request.user,
                    video=get_object_or_404(Video, id=video_id),
                    defaults={
                        'reaction': serializer.validated_data['reaction']
                    }
                )

                if created:
                    return Response(
                        serializer.data, status=status.HTTP_201_CREATED
                    )

                if not created:
                    reaction_obj.reaction = \
                        serializer.validated_data['reaction']
                    reaction_obj.save()

                    return Response(
                        serializer.data, status=status.HTTP_200_OK
                    )
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            return Response(
                {'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST
            )
