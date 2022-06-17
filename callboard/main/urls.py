from django.urls import path, include
from .views import AdvList, AdvDetailView, AdvCreateView, UserView, Accept, AdvDeleteView, Cans, AdvEditView

urlpatterns = [
    path('', AdvList.as_view()),
    path('<int:pk>/', AdvDetailView.as_view(), name='adv_detail'),
    path('<int:pk>/delete/', AdvDeleteView.as_view(), name='adv_delete'),
    path('<int:pk>/edit/', AdvEditView.as_view(), name='adv_edit'),
    path('accept/<int:pk>/', Accept.as_view(), name='resp_accept'),
    path('cancel/<int:pk>/', Cans.as_view(), name='resp_cancel'),
    path('add/', AdvCreateView.as_view(), name='adv_create'),
    path('account/', UserView.as_view(), name='account'),
]