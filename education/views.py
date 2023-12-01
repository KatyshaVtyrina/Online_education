
from django_filters.rest_framework import DjangoFilterBackend


from rest_framework import viewsets, generics, status
from rest_framework.exceptions import APIException
from rest_framework.filters import OrderingFilter
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from education.models import Course, Lesson, Payments, Subscription
from education.paginators import CoursePaginator, LessonPaginator
from education.permissions import IsStaff, IsOwner, IsOwnerOrIsStaff
from education.serializers import CourseSerializer, LessonSerializer, PaymentSerializer, LessonCreateSerializer, \
    SubscriptionSerializer, SubscriptionCreateSerializer, PaymentCreateSerializer, PaymentDetailSerializer
from education.services import stripe_create_session, stripe_retrieve_session


class CourseViewSet(viewsets.ModelViewSet):
    """Контроллер для модели Course"""
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

    def perform_create(self, serializer):
        """Автоматическое сохранение владельца при создании объекта"""
        new_course = serializer.save()
        new_course.owner = self.request.user
        new_course.save()


class LessonCreateAPIView(generics.CreateAPIView):
    """Создание урока"""
    serializer_class = LessonCreateSerializer
    permission_classes = [~IsStaff]

    def perform_create(self, serializer):
        """Автоматическое сохранение владельца при создании объекта"""
        new_lesson = serializer.save()
        new_lesson.owner = self.request.user
        new_lesson.save()


class LessonListAPIView(generics.ListAPIView):
    """Просмотр списка уроков"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.filter()
    pagination_class = LessonPaginator


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр детальной информации об уроке"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrIsStaff]


class LessonUpdateAPIView(generics.UpdateAPIView):
    """Обновление урока"""
    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = [IsOwnerOrIsStaff]


class LessonDestroyAPIView(generics.DestroyAPIView):
    """Удаление урока"""
    queryset = Lesson.objects.all()
    permission_classes = [IsOwner]


class PaymentCreateAPIView(generics.CreateAPIView):
    """Создание платежа"""
    serializer_class = PaymentCreateSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        try:
            course = serializer.validated_data['course']
            user = request.user

            session = stripe_create_session(course, user)
            payment = Payments.objects.create(
                course=course,
                user=user,
                session_id=session.id
            )
            payment_serializer = PaymentCreateSerializer(payment)
            return Response(payment_serializer.data, status=status.HTTP_201_CREATED)

        except Payments.DoesNotExist:
            raise APIException(detail='Платеж не найден')


class PaymentListAPIView(generics.ListAPIView):
    """Просмотр списка платежей"""
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ('course', 'is_paid')
    ordering_fields = ('date_of_payment', 'is_paid')


class PaymentRetrieveAPIView(generics.RetrieveAPIView):
    """Просмотр детальной информации о платеже"""
    serializer_class = PaymentDetailSerializer
    queryset = Payments.objects.all()

    def get_object(self):
        """Меняет статус оплаты, если оплачено"""
        payment = get_object_or_404(self.get_queryset(), pk=self.kwargs['pk'])
        if payment.session_id:
            session = stripe_retrieve_session(payment.session_id)
            if session.payment_status in ['paid', 'complete']:
                payment.is_paid = True
                payment.save()
        return payment


class PaymentUpdateAPIView(generics.UpdateAPIView):
    """Обновление платежа"""
    serializer_class = PaymentSerializer
    queryset = Payments.objects.all()


class PaymentDestroyAPIView(generics.DestroyAPIView):
    """Удаление платежа"""
    queryset = Payments.objects.all()


class SubscriptionCreateAPIView(generics.CreateAPIView):
    """Создание подписки"""
    serializer_class = SubscriptionCreateSerializer

    def perform_create(self, serializer):
        """Автоматическое сохранение владельца при создании объекта"""
        subscription = serializer.save()
        subscription.user = self.request.user
        subscription.save()


class SubscriptionDestroyAPIView(generics.DestroyAPIView):
    """Удаление подписки"""
    serializer_class = SubscriptionSerializer
    queryset = Subscription.objects.all()
