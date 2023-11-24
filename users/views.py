from rest_framework import generics, viewsets
from rest_framework.response import Response

from users.models import User
from users.permissions import IsUser
from users.serializers import UserSerializer, ProfileUserSerializer


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        if self.request.user == self.get_object():
            serializer_class = UserSerializer
        else:
            serializer_class = ProfileUserSerializer

        serializer = serializer_class(self.get_object())
        serializer_data = serializer.data

        return Response(serializer_data)

    def get_permissions(self):
        permission_classes = []
        if self.action in ['update', 'partial_update']:
            permission_classes = [IsUser]
        return [permission() for permission in permission_classes]
