from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.db import IntegrityError
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView
from django.views.generic.edit import FormMixin, ModelFormMixin
from django_filters.views import FilterMixin

from .models import Advertisement, Response
from .filters import AdvFilter, AccountFilter
from .forms import AdvForm, RespForm
from django.shortcuts import redirect, render

from sign.models import UserCode


def check_valid(self):
    print('post')
    if self.request.user.is_authenticated:
        if not UserCode.objects.filter(user_id=self.request.user).values('valid')[0]['valid']:
            print('da!!')
            self.request.user.delete()
    return redirect('/adv/')


class AdvList(ListView):
    model = Advertisement
    template_name = 'advertisements.html'
    context_object_name = 'advs'
    queryset = Advertisement.objects.order_by('-time_create')

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = AdvFilter(self.request.GET, queryset=self.get_queryset())
        check_valid(self)
        return context


class AdvDetailView(FormMixin, DetailView):
    model = Advertisement
    template_name = 'advertisement_detail.html'
    context_object_name = 'adv'
    form_class = RespForm
    queryset = Advertisement.objects.all()

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        pk = self.kwargs.get('pk')
        if form.is_valid():
            return self.form_valid(form)

    def form_valid(self, form, **kwargs):
        try:
            self.object = form.save(commit=False)
            self.object.user = self.request.user
            self.object.post = self.get_object()
            self.object.save()
            return super().form_valid(form)
        except IntegrityError:
            return redirect('/adv/')

    def get_success_url(self, **kwargs):
        check_valid(self)
        return reverse_lazy('adv_detail', kwargs={'pk': self.get_object().id})

class AdvEditView(LoginRequiredMixin, CreateView):
    template_name = 'advertisement_create.html'
    form_class = AdvForm

class AdvCreateView(LoginRequiredMixin, CreateView):
    template_name = 'advertisement_create.html'
    form_class = AdvForm
    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Advertisement.objects.get(pk=id)

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        check_valid(self)
        return initial

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('/adv/')


class AdvDeleteView(DeleteView):
    template_name = 'advertisement_delete.html'
    permission_required = ('main.delete_adv',)
    queryset = Advertisement.objects.all()
    context_object_name = 'adv'
    success_url = '/adv/'


class UserView(ListView):
    model = Advertisement
    template_name = 'account.html'
    context_object_name = 'advs'
    queryset = Response.objects.order_by('-time_create')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = AccountFilter(self.request.GET, queryset=self.get_queryset())
        check_valid(self)
        return context

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user
        return initial


class Accept(UpdateView):
    model = Response
    template_name = 'accept.html'
    form_class = RespForm

    def get_context_data(self, **kwargs):
        check_valid(self)
        context = super().get_context_data(**kwargs)
        context['messege'] = 'Вы приняли отклик!'
        id = self.kwargs.get('pk')
        Response.objects.filter(pk=id).update(accepted=True)
        user = self.object.user
        send_mail(
            subject='Вас выбрали!',
            message=f'Пользователь выбрал ваш отклик.',
            from_email='dkizimasf@yandex.ru',
            recipient_list=[User.objects.filter(username=user).values("email")[0]['email']]
        )
        return context


class Cans(UpdateView):
    model = Response
    template_name = 'accept.html'
    form_class = RespForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['messege'] = 'Вы отменили отклик!'
        id = self.kwargs.get('pk')
        Response.objects.filter(pk=id).update(accepted=False)
        check_valid(self)
        return context
