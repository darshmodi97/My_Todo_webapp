from django.contrib import admin

# Register your models here.
from todo.models import ToDo as myToDo, ToDoLog


class ToDoAdmin(admin.ModelAdmin):
    list_display = ['name', 'due_date', 'get_users', 'status', ]
    search_fields = ['user', 'name']
    list_filter = ['status', ]

    def get_users(self, obj):
        return obj.user.all()


admin.site.register(myToDo, ToDoAdmin)
admin.site.register(ToDoLog)
