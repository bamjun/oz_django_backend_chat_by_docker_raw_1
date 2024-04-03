from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Video
from .serializers import VideoSerializer
from rest_framework.exceptions import NotFound
from rest_framework import status
from .services import VideoService


# 1.VideoList
# api/v1/videos
# - GET: 전체 비디오 목록 조회 => Video.objects.all() => 클라이언트에 전달
# - POST: 새로운 비디오 생성
# - DELETE, PUT: X
class VideoList(APIView):
    def get(self, request):
        videos = Video.objects.all()

        serializer = VideoSerializer(videos, many=True)

        return Response(serializer.data)

    def post(self, request):
        try:
            user_data = request.data
            serializer = VideoSerializer(data=user_data)

            if serializer.is_valid():
                serializer.save(user=request.user)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    serializer.errors, status=status.HTTP_400_BAD_REQUEST
                )

        except Exception as e:
            return Response(
                {'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST
            )


# 2.VideoDetail
# api/v1/videos/{video_id}
# - GET: 특정 비디오 상세 조회
# - POST: X
# - PUT: 특정 비디오 정보 업데이트(수정)
# - DELETE: 특정 비디오 삭제
class VideoDetail(APIView):
    def get_object(self, pk):
        try:
            return Video.objects.get(pk=pk)
        except Video.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        VideoService.increase_view_count(video_id=pk)
        video = self.get_object(pk)
        serializer = VideoSerializer(video)
        like_count = VideoService.get_like_count(video_id=pk)
        dislike_count = VideoService.get_dislike_count(video_id=pk)
        subscriber_count = VideoService.get_subscriber_count(
            video_owner=video.user
            )
        is_subscribed = VideoService.get_is_subscribed(
            user_id=request.user, video_owner=video.user
            )
        reaction = VideoService.get_reaction(user_id=request.user, video_id=pk)
        data = {
            'video_info': serializer.data,
            'like_count': like_count,
            'dislike_count': dislike_count,
            'subscriber_count': subscriber_count,
            'is_subscribed': is_subscribed,
            'reaction': reaction
        }
        return Response(data, status=status.HTTP_200_OK)

    def put(self, request, pk):
        video = self.get_object(pk)
        user_data = request.data

        try:
            serializer = VideoSerializer(video, data=user_data)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {'msg': str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, pk):
        video = self.get_object(pk)
        video.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)
