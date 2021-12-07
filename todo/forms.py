from datetime import datetime

from django import forms
from django.core.exceptions import ValidationError
from django.forms import SelectDateWidget

from todo.models import ToDo


class ToDoFormView(forms.ModelForm):
    due_date= forms.DateField(widget=SelectDateWidget(empty_label="Nothing"))
    class Meta:
        model = ToDo
        exclude = ['user', ]

    def clean_due_date(self):
        due_date= self.cleaned_data.get('due_date')
        print(due_date,"========")
        if due_date < datetime.today().date():
            raise ValidationError('Please choose correct date')
        return due_date