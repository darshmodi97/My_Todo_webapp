from django.contrib.auth.models import User
from django.db import models


# Create your models here.

class TimeStampModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class ToDo(TimeStampModel):
    ACTIVE = "Active"
    COMPLETED = "Completed"
    STATUS_CHOICES = [
        (ACTIVE, "Active"),
        (COMPLETED, "Completed"),
    ]
    name = models.CharField(max_length=1024, null=True, blank=True)
    user = models.ManyToManyField(User, verbose_name="Created By", related_name="users")
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default=ACTIVE)
    due_date = models.DateField()
    owner = models.ForeignKey(User, related_name="todos", on_delete=models.CASCADE, null=True, blank=True)
    class Meta:
        verbose_name_plural = "To-Dos"

    def __str__(self):
        return self.name


class ToDoLog(TimeStampModel):
    updated_by = models.ForeignKey(User, related_name="todologs", on_delete=models.CASCADE)
    todo = models.ForeignKey(ToDo, related_name="todos", on_delete=models.CASCADE)

    def __str__(self):
        return f"Todo updated by {self.updated_by}"
