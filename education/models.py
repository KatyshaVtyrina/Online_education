from django.db import models

from config import settings


NULLABLE = {'blank': True, 'null': True}


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(verbose_name='картинка', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)
    price = models.PositiveIntegerField(default=50000, verbose_name='цена')

    def __str__(self):
        return f'Название курса - {self.title}'

    class Meta:
        verbose_name = 'курс'
        verbose_name_plural = 'курсы'

    @property
    def stripe_price_data(self) -> dict:
        return {
            'currency': 'usd',
            'unit_amount': self.price,
            'product_data': {
                'name': self.title,
            },
        }


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    preview = models.ImageField(verbose_name='картинка', **NULLABLE)
    description = models.TextField(verbose_name='описание', **NULLABLE)
    url = models.URLField(verbose_name='ссылка на видео', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='владелец', **NULLABLE)

    def __str__(self):
        return f'Название урока - {self.title}'

    class Meta:
        verbose_name = 'урок'
        verbose_name_plural = 'уроки'


class Payments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    date_of_payment = models.DateField(auto_now_add=True, verbose_name='дата оплаты', **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='payments', **NULLABLE)
    session_id = models.CharField(max_length=150, editable=False, verbose_name='id сессии', **NULLABLE)
    is_paid = models.BooleanField(default=False, verbose_name='статус платежа')

    def __str__(self):
        return f'Курс - {self.course}, статус оплаты - {self.is_paid}'

    class Meta:
        verbose_name = 'платеж'
        verbose_name_plural = 'платежи'


class Subscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='subscription', verbose_name='курс')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name='пользователь', **NULLABLE)
    is_subscription = models.BooleanField(default=True, verbose_name='признак подписки')

    def __str__(self):
        return f'{self.user} - {self.course}: {self.is_subscription}'

    class Meta:
        verbose_name = 'подписка'
        verbose_name_plural = 'подписки'
