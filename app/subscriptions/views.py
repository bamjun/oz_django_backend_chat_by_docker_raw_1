from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Subscription
from .serializers import SubSerializer
# from rest_framework.exceptions import NotFound
from rest_framework import status
from django.shortcuts import get_object_or_404


class SubscriptionList(APIView):
    def post(self, request):
        data = {
            'subscriber': request.user.pk,
            'subscribed_to': request.data['subscribed_to']
        }
        try:
            serializer = SubSerializer(data=data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()
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

    def get(self, request):
        subs = Subscription.objects.all()
        serializer = SubSerializer(subs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class SubscriptionDetail(APIView):
    def delete(self, request, pk):
        sub = get_object_or_404(
            Subscription, subscriber=request.user, subscribed_to=pk
        )
        sub.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
