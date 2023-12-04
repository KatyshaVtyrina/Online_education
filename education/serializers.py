from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from education.models import Course, Lesson, Payments, Subscription
from education.services import stripe_retrieve_session
from education.validators import UrlValidator
from users.models import User


class LessonCreateSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для создания урока"""
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            UrlValidator(field='url')
        ]


class LessonSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели Lesson"""

    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())
    owner = SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [
            UrlValidator(field='url')
        ]


class CourseSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели Course"""
    # количество уроков у курса
    count_lessons = serializers.IntegerField(source='lesson_set.all.count', read_only=True)
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)
    owner = SlugRelatedField(slug_field='email', queryset=User.objects.all())
    subscription =serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = '__all__'

    def get_subscription(self, obj):
        request = self.context.get('request')
        if request:
            user = request.user
            subscription = Subscription.objects.filter(course=obj, user=user).first()
            if subscription:
                return subscription.is_subscription
            return False
        return False


class PaymentSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели Payment"""
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())
    user = SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Payments
        fields = '__all__'


class PaymentCreateSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для создания модели Payment"""
    payment_link = serializers.SerializerMethodField()

    class Meta:
        model = Payments
        fields = '__all__'

    def get_payment_link(self, payment: Payments):
        session = stripe_retrieve_session(payment.session_id)
        return session.url


class PaymentDetailSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для просмотра детальной информации по объекту Payment"""
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())
    payment_link = serializers.SerializerMethodField()
    user = SlugRelatedField(slug_field='email', queryset=User.objects.all())

    class Meta:
        model = Payments
        fields = '__all__'

    def get_payment_link(self, payment: Payments):
        """Получает ссылку на оплату"""
        session = stripe_retrieve_session(payment.session_id)
        return session.url


class LessonListSerializer(serializers.ModelSerializer):
    """Класс-сериализатор просмотра списка уроков модели Lesson"""
    class Meta:
        model = Lesson
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели Subscription"""
    class Meta:
        model = Subscription
        fields = '__all__'


class SubscriptionCreateSerializer(serializers.ModelSerializer):
    """Класс-сериализатор создания подписки модели Subscription"""
    class Meta:
        model = Subscription
        fields = '__all__'

    def validate(self, attrs):
        user = self.context['request'].user
        course = attrs['course']
        subscription = Subscription.objects.filter(user=user, course=course, is_subscription=True).exists()

        if subscription:
            raise serializers.ValidationError(f"Подписка уже существует.")

        return attrs
