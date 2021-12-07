from django.urls import path

from todo import views

app_name = 'todo'

urlpatterns = [
    path('list/', views.ToDoListView.as_view(), name='todo-list'),
    path('create/', views.create_todo, name='create_todo'),
    path('edit/<int:pk>/', views.update_todo, name='update'),
    path('delete/<int:pk>/', views.delete_todo, name='delete'),
    path('share/', views.share_todo, name='share_todo'),

]
