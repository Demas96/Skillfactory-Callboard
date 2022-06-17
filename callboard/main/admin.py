from django.contrib import admin

from django import forms
from .models import Advertisement, Category, Response
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class AdvAdminForm(forms.ModelForm):
    # video_link = forms.CharField(widget=CKEditorUploadingWidget())

    class Meta:
        model = Advertisement
        fields = '__all__'


class AdvAdmin(admin.ModelAdmin):
    form = AdvAdminForm


admin.site.register(Advertisement, AdvAdmin)
admin.site.register(Category)
admin.site.register(Response)
