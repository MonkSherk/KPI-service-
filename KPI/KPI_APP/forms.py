from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Task, Task_Answer, User, departments

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'deadline', 'priority', 'status', 'assigned_to', 'department']

class TaskAnswerForm(forms.ModelForm):
    class Meta:
        model = Task_Answer
        fields = ['answer', 'file']

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = 'username', 'password1', 'password2' , 'role'
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = departments
        fields = ['name', 'users']

from django import forms
from .models import Task, User, departments

class TaskFilterForm(forms.Form):
    title = forms.CharField(required=False, label='Название задачи')
    status = forms.ChoiceField(choices=Task.STATUS_CHOICES, required=False, label='Статус')
    assigned_to = forms.ModelChoiceField(queryset=User.objects.all(), required=False, label='Назначено')
    department = forms.ModelChoiceField(queryset=departments.objects.all(), required=False, label='Отдел')