from django.forms import ModelForm
from .models import Advertisement, Response
from django import forms


class AdvForm(ModelForm):
    header = forms.CharField(label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-input'}))
    text = forms.CharField(label='Текст', widget=forms.TextInput(attrs={'class': 'form-input'}))
    video_link = forms.CharField(label='Ссылка на видео YouTube', widget=forms.TextInput(attrs={'class': 'form-input'}), required=False)
    image = forms.ImageField(label='Изображение', required=False)

    class Meta:
        model = Advertisement
        fields = ['user', 'header', 'text', 'video_link', 'category', 'image']
        widgets = {
            'user': forms.HiddenInput(),
        }

class RespForm(ModelForm):
    resp_text = forms.CharField(label='Текст', widget=forms.TextInput(attrs={'class': 'form-input'}))
    class Meta:
        model = Response
        fields = ('resp_text',)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
