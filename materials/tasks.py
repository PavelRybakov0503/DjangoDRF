from django.core.mail import send_mail
from celery import shared_task
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import get_user_model


@shared_task
def send_course_update_email(user_email, course_title, update_type):
    send_mail(
        subject=f'Обновление курса: {course_title}',
        message=f'В вашем курсе "{course_title}" появилось новое обновление: {update_type}.',
        from_email='noreply@yourdomain.com',
        recipient_list=[user_email],
    )


@shared_task
def deactivate_inactive_users():
    User = get_user_model()
    month_ago = timezone.now() - timedelta(days=30)
    users_to_deactivate = User.objects.filter(
        last_login__lt=month_ago,
        is_active=True
    )
    users_to_deactivate.update(is_active=False)
