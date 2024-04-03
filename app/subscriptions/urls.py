from django.urls import path
from . import views


urlpatterns = [
    path('', views.SubscriptionList.as_view(), name='subs-list'),
    path('<int:pk>', views.SubscriptionDetail.as_view(), name='subs-detail'),
]
