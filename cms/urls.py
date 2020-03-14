from django.urls import path
from . import views

app_name = 'cms'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('user_manage/', views.Manage.as_view(), name='manage'),
]