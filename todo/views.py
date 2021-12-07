from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.db import transaction
from django.http import JsonResponse
from django.shortcuts import render, redirect
# Create your views here.
from django.views.generic import ListView, UpdateView

from todo.forms import ToDoFormView
from todo.models import ToDo, ToDoLog


@login_required(login_url='login/')
@transaction.atomic
def create_todo(request):
    if request.method == 'POST':
        form = ToDoFormView(request.POST)

        if form.is_valid():
            todo = form.save(commit=False)
            todo.owner = request.user
            todo.save()
            todo.user.add(request.user)
            return redirect('/')
        else:
            messages.error(request, f"{form.errors['due_date']}")

        return render(request, 'todo/create_todo.html', {'form': form})
    else:
        form = ToDoFormView()
        return render(request, 'todo/create_todo.html', {'form': form})


@login_required(login_url='login/')
def update_todo(request, pk):
    data = ToDo.objects.get(id=pk)
    if request.method == 'POST':
        data.name = request.POST.get('name')
        data.status = request.POST.get('status')
        data.due_date = request.POST.get('due_date')
        data.save()
        ToDoLog.objects.create(updated_by=request.user, todo=data)
        messages.success(request, 'Your To-Do updated successfully.')
        return redirect('todo:todo-list')
    return render(request, 'todo/edit_todo.html', {'data': data})


class ToDoListView(LoginRequiredMixin, ListView):
    model = ToDo
    template_name = 'todo/todolist.html'
    paginate_by = 20

    def get_queryset(self):
        return ToDo.objects.filter(user=self.request.user).order_by('-id', 'status')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ToDoListView, self).get_context_data()
        context['users'] = User.objects.exclude(username=self.request.user.username)
        context['todo_logs'] = ToDoLog.objects.filter(todo__owner=self.request.user).order_by('-id', 'todo__status')
        return context


def delete_todo(request, pk):
    if request.is_ajax():
        data = ToDo.objects.get(id=pk).delete()
        return JsonResponse({'status': 'success', 'id': pk, 'count': ToDo.objects.count()})
    else:
        msg = "Something went wrong"
        return JsonResponse({'status': 'failed', 'msg': msg})


def share_todo(request):
    if request.method == 'POST':
        user_ids = request.POST.getlist('user_ids')
        todo_id = request.POST.get('todo')

        users = User.objects.filter(id__in=user_ids)

        todo = ToDo.objects.get(id=todo_id)
        for user in users:
            todo.user.add(user)
        messages.success(request, "shared successful.")
        return redirect('/')
