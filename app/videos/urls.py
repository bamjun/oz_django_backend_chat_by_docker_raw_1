from django.urls import path
from . import views
from reactions.views import ReactionDetail
from comments.views import CommentList

urlpatterns = [
    path('', views.VideoList.as_view(), name='video-list'),
    path('<int:pk>/', views.VideoDetail.as_view(), name='video-detail'),
    path(
        '<int:video_id>/reaction',
        ReactionDetail.as_view(),
        name='video-reaction'
        ),
    path(
        '<int:video_id>/comment',
        CommentList.as_view(),
        name='video-comment'
        ),
    # path('upload/', views.VideoUpload.as_view(), name='video-upload')
]
