from django_filters import FilterSet, ChoiceFilter
from .models import Advertisement, Response
from django import forms


class AdvFilter(FilterSet):
    class Meta:
        model = Advertisement
        fields = ('category',)


class AccountFilter(FilterSet):
    class Meta:
        model = Response
        fields = ('accepted',)
