from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class Roles(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class User(AbstractUser):
    # role_choice = {
    #     ('owner', 'Owner'),
    #     ('employee', 'Employee'),
    # }
    role = models.ForeignKey(Roles, on_delete=models.CASCADE , null=True, blank=True)

    def __str__(self):
        return self.username

class departments(models.Model):
    name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name='departments')

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ('not completed', 'Не выполнено'),
        ('completed', 'Выполнено'),
        ('dead', 'Просрочено'),
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    deadline = models.DateTimeField()
    priority = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')
    department = models.ForeignKey('departments', on_delete=models.CASCADE)

class Notification(models.Model):
    text = models.CharField(max_length=255)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(max_length=20)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)

class Task_Answer(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    file = models.FileField(upload_to='answers/', null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')


