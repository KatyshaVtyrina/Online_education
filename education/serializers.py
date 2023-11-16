from rest_framework import serializers

from education.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели Lesson"""
    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    """Класс-сериализатор для модели Course"""
    # количество уроков у курса
    count_lessons = serializers.IntegerField(source='lesson_set.all.count')
    lessons = LessonSerializer(source='lesson_set', many=True)

    class Meta:
        model = Course
        fields = '__all__'
