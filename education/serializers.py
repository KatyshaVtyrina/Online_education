from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from education.models import Course, Lesson, Payments, Subscription
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
            return "Подписка не создавалась"
        return False


class PaymentSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели Payment"""
    course = SlugRelatedField(slug_field='title', queryset=Course.objects.all())
    lesson = SlugRelatedField(slug_field='title', queryset=Lesson.objects.all())

    class Meta:
        model = Payments
        fields = ('id', 'date_of_payment', 'amount', 'payment_method', 'course', 'lesson')


class LessonListSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели Lesson"""
    class Meta:
        model = Lesson
        fields = '__all__'


class SubscriptionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Subscription
        fields = '__all__'


class SubscriptionCreateSerializer(serializers.ModelSerializer):

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

