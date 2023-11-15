from django.urls import path
from rest_framework.routers import DefaultRouter
from users.apps import UsersConfig
from users.views import UserViewSet

app_name = UsersConfig

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')


urlpatterns = [
    # path('user/register/', UserRegisterAPIView.as_view(), name='register'),
    # path('user/update/<int:pk>/', UserProfileAPIView.as_view(), name='user_profile'),
    # path('user/delete/<int:pk>/', UserDestroyAPIView.as_view(), name='user_delete'),
] + router.urls
