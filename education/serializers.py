from rest_framework import serializers

from education.models import Course, Lesson, Payments


class LessonSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели Lesson"""
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели Course"""
    # количество уроков у курса
    count_lessons = serializers.IntegerField(source='lesson_set.all.count', read_only=True)
    lessons = LessonSerializer(source='lesson_set', many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели Payment"""

    class Meta:
        model = Payments
        fields = '__all__'


class LessonListSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели Lesson"""
    class Meta:
        model = Lesson
        fields = '__all__'