from django.contrib import admin

from education.models import Subscription, Course, Lesson, Payments


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview', 'description', 'owner', 'price')
    search_fields = ('title',)
    list_filter = ('title',)


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'preview', 'description', 'url', 'course', 'owner')
    search_fields = ('title',)
    list_filter = ('title',)


@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'date_of_payment', 'course', 'session_id', 'is_paid')
    search_fields = ('user',)
    list_filter = ('user', 'date_of_payment')


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('course', 'user', 'is_subscription')
    search_fields = ('course', 'user')
    list_filter = ('user', 'course')
