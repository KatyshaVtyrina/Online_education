from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from education.models import Course, Lesson, Payments
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

    class Meta:
        model = Course
        fields = '__all__'


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
