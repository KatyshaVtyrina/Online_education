from django.urls import path

from education.apps import EducationConfig
from rest_framework.routers import DefaultRouter

from education.views import (CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView,
                             LessonUpdateAPIView, LessonDestroyAPIView, PaymentListAPIView, PaymentCreateAPIView,
                             PaymentRetrieveAPIView, PaymentUpdateAPIView, PaymentDestroyAPIView,
                             SubscriptionCreateAPIView, SubscriptionDestroyAPIView)

app_name = EducationConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
    path('lessons/', LessonListAPIView.as_view(), name='lessons_list'),
    path('lesson/create/', LessonCreateAPIView.as_view(), name='lesson_create'),
    path('lesson/<int:pk>/', LessonRetrieveAPIView.as_view(), name='lesson_retrieve'),
    path('lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='lesson_update'),
    path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),

    path('payments/', PaymentListAPIView.as_view(), name='payments_list'),
    path('payment/create/', PaymentCreateAPIView.as_view(), name='payment_create'),
    path('payment/<int:pk>/', PaymentRetrieveAPIView.as_view(), name='payment_retrieve'),
    path('payment/update/<int:pk>/', PaymentUpdateAPIView.as_view(), name='payment_update'),
    path('payment/delete/<int:pk>/', PaymentDestroyAPIView.as_view(), name='payment_delete'),

    path('course/subscription/create/', SubscriptionCreateAPIView.as_view(), name='subscription_create'),
    path('course/subscription/delete/<int:pk>/', SubscriptionDestroyAPIView.as_view(), name='subscription_delete')
] + router.urls
