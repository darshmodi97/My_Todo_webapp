from django.contrib import auth
from django.urls import path

from users import views
from users.views import activate

app_name = 'users'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.Login, name='login'),
    path('register/', views.signup, name='register'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
         activate, name='activate'),
    path('logout/', views.LogoutView, name='logout'),

]
