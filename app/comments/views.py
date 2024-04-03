from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Video
from users.models import User
from .serializers import CommentSerializer
from rest_framework import status
from django.shortcuts import get_object_or_404
from videos.services import VideoService


class CommentList(APIView):
    def post(self, request, video_id):
        user_data = request.data
        try:
            serializer = CommentSerializer(data=user_data)

            if serializer.is_valid(raise_exception=True):
                serializer.save(
                    user=get_object_or_404(User, id=request.user.id),
                    video=get_object_or_404(Video, id=video_id)
                )

                return Response(
                    serializer.data,
                    status=status.HTTP_201_CREATED
                )

            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(
                {'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    def get(self, request, video_id):
        comment_list = VideoService.get_comment_list(video_id=video_id)
        comment_count = VideoService.get_comment_count(video_id=video_id)
        serializer = CommentSerializer(comment_list, many=True)
        data = {
            'comment_list': serializer.data,
            'comment_count': comment_count
        }

        return Response(data, status=status.HTTP_200_OK)


class CommentDetail(APIView):
    pass
