from django.contrib import admin
from .models import Roles, User, departments, Notification, Task, Task_Answer

admin.site.register(Roles)
admin.site.register(User)
admin.site.register(departments)
admin.site.register(Notification)
admin.site.register(Task)
admin.site.register(Task_Answer)
