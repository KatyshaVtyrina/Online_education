from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, generics
from rest_framework.filters import OrderingFilter

from education.models import Course, Lesson, Payments, Subscription
from education.paginators import CoursePaginator, LessonPaginator
from education.permissions import IsStaff, IsOwner, IsOwnerOrIsStaff
from education.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, LessonCreateSerializer, \
    SubscriptionSerializer


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = CoursePaginator

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [~IsStaff]
        elif self.action in ['retrieve', 'update', 'partial_update']:
            permission_classes = [IsOwnerOrIsStaff]
        elif self.action == 'destroy':
            permission_classes = [IsOwner]
        return [permission() for permission in permission_classes]


class LessonCreateAPIView(generics.CreateAPIView):
    serializer_class = LessonCreateSerializer
    permission_classes = [~IsStaff]

    def perform_create(self, serializer):
        """Автоматическое сохранение владельца при создании объекта"""
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.filter()
    pagination_class = LessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrIsStaff]


class LessonUpdateAPIView(generics.UpdateAPIView):
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrIsStaff]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удалить может только владелец"""
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class PaymentCreateAPIView(generics.CreateAPIView):
    serializer_class = PaymentSerializer


class PaymentListAPIView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'lesson', 'payment_method')
    ordering_fields = ('date_of_payment', )


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()


class PaymentUpdateAPIView(generics.UpdateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()


class PaymentDestroyAPIView(generics.DestroyAPIView):
    queryset = Payments.objects.all()
