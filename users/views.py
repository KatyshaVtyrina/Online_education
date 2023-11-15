from rest_framework import generics, viewsets

from users.models import User
from users.serializers import UserSerializer


# class UserRegisterAPIView(generics.CreateAPIView):
#     serializer_class = UserSerializer
#
#
# class UserProfileAPIView(generics.UpdateAPIView):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()
#
#
# class UserDestroyAPIView(generics.DestroyAPIView):
#     serializer_class = UserSerializer
#     queryset = User.objects.all()

class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()
