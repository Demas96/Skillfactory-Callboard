import datetime
from django.db.models.signals import post_save, pre_save, m2m_changed, post_init
from django.dispatch import receiver
from django.template.loader import render_to_string
from .models import Response, Advertisement
from django.core.mail import EmailMultiAlternatives, send_mail
from django.contrib.auth.models import User


@receiver(post_save, sender=Response)
def send_mail_resp(sender, instance, created, **kwargs):
    if created:
        user = Advertisement.objects.get(pk=instance.post_id).user
        send_mail(
            subject='Новый отклик',
            message=f'{instance.user} оставил отклик на Ваше обьявление: {instance.resp_text}',
            from_email='dkizimasf@yandex.ru',
            recipient_list=[User.objects.filter(username=user).values("email")[0]['email']],
        )

