from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f'{self.category}'


class Advertisement(models.Model):
    header = models.CharField(max_length=255)
    text = models.TextField()
    video_link = models.TextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Категория')
    time_create = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='advertisement_user')
    image = models.ImageField(upload_to='images/', null=True, blank=True)

    def __str__(self):
        return f'{self.header}'

    def get_absolute_url(self):
        return f'/adv/{self.id}'


class Response(models.Model):
    post = models.ForeignKey(Advertisement, on_delete=models.CASCADE, related_name='response_advertisement')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    resp_text = models.CharField(max_length=255,  verbose_name='Текст')
    time_create = models.DateTimeField(auto_now_add=True)
    accepted = models.BooleanField(default=False, verbose_name='Принято')

    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return f'{self.resp_text}'

    def is_accept(self):
        return self.accepted
