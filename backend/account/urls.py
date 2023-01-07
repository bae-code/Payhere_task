from django.urls import path
from .views import *

urlpatterns = [
    path('account-book/list', AccountBookListView.as_view(), name='account-book-list'),
    path('account-book/<int:pk>', AccountBookDetailView.as_view(), name='account-book-detail'),
    path('account-book/register', AccountBookRegisterView.as_view(), name='account-book-create'),
    path('account-book/clone/<int:pk>', AccountBookCloneView.as_view(), name='account-book-clone'),
    path('account-book/share/<int:pk>', AccountBookShareView.as_view(), name='account-book-share'),
]
