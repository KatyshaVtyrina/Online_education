
from django.core.mail import send_mail


from config import settings
from config.celery import app
from education.models import Subscription, Course


@app.task
def send_notification_update_course(course_id):
    subscribers = Subscription.objects.filter(course=course_id, is_subscription=True)
    course = Course.objects.get(id=course_id)

    for subscriber in subscribers:
        send_mail(
            subject=f'Обновление курса {course.title}',
            message=f'Курс {course.title}, на который вы подписаны, обновлен',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[subscriber.user.email],
            fail_silently=False
        )
        print(f'Письмо отправлено {subscriber.user.email}')
