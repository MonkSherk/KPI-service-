from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView

from .models import Task, Task_Answer, Notification, User, departments
from .forms import TaskForm, TaskAnswerForm, UserForm, DepartmentForm, TaskFilterForm


@method_decorator(login_required(login_url='login_page'), name='dispatch')
class TaskListView(View):
    def get(self, request):
        form = TaskFilterForm(request.GET)
        if request.user.role.name == "Руководитель":
            tasks = Task.objects.all()
        else:
            tasks = Task.objects.filter(assigned_to=request.user)

        if form.is_valid():
            if form.cleaned_data['title']:
                tasks = tasks.filter(title__icontains=form.cleaned_data['title'])
            if form.cleaned_data['status']:
                tasks = tasks.filter(status=form.cleaned_data['status'])
            if form.cleaned_data['assigned_to']:
                tasks = tasks.filter(assigned_to=form.cleaned_data['assigned_to'])
            if form.cleaned_data['department']:
                tasks = tasks.filter(department=form.cleaned_data['department'])

        return render(request, 'task_list.html', {'tasks': tasks, 'form': form})


@method_decorator(login_required(login_url='login_page'), name='dispatch')
class TaskDetailView(View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskAnswerForm()
        return render(request, 'task_detail.html', {'task': task, 'form': form})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskAnswerForm(request.POST, request.FILES)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.task = task
            answer.user = request.user
            answer.author = request.user
            answer.save()
            task.status = 'completed'
            task.save()
            Notification.objects.create(
                text=f"Задача '{task.title}' выполнена пользователем {request.user.username}.",
                user=task.created_by,
                type="task",
                task=task
            )
            # Уменьшаем количество задач
            request.user.profile.task_count -= 1
            request.user.profile.save()
            return redirect('task-list')
        return render(request, 'task_detail.html', {'task': task, 'form': form})

    def put(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        if request.user.role.name == "Руководитель":
            task.rating = request.POST.get('rating')
            task.save()
            Notification.objects.create(
                text=f"Задача '{task.title}' была оценена руководителем {request.user.username}.",
                user=task.assigned_to,
                type="task",
                task=task
            )
            return redirect('task-list')
        return render(request, 'task_detail.html', {'task': task})


@method_decorator(login_required(login_url='login_page'), name='dispatch')
class TaskCreateView(View):
    def get(self, request):
        form = TaskForm()
        return render(request, 'task_form.html', {'form': form})

    def post(self, request):
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.created_by = request.user
            task.save()
            Notification.objects.create(
                text=f"Новая задача '{task.title}' назначена пользователю {task.assigned_to.username}.",
                user=task.assigned_to,
                type="task"
            )
            # Увеличиваем количество задач
            request.user.profile.task_count += 1
            request.user.profile.save()
            return redirect('task-list')
        return render(request, 'task_form.html', {'form': form})


@method_decorator(login_required(login_url='login_page'), name='dispatch')
class TaskUpdateView(View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(instance=task)
        return render(request, 'task_form.html', {'form': form})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            task = form.save()
            Notification.objects.create(
                text=f"Задача '{task.title}' была изменена.",
                user=task.assigned_to,
                type="task"
            )
            return redirect('task-list')
        return render(request, 'task_form.html', {'form': form})


@method_decorator(login_required(login_url='login_page'), name='dispatch')
class TaskDeleteView(View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        return render(request, 'task_confirm_delete.html', {'task': task})

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        task.delete()
        return redirect('task-list')


class TaskCompletedView(View):
    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk, status='completed', created_by=request.user)
        answers = Task_Answer.objects.filter(task=task)  # Directly filter Task_Answer by task
        return render(request, 'task_completed_detail.html', {'task': task, 'answers': answers})


@method_decorator(login_required(login_url='login_page'), name='dispatch')
class UserListView(View):
    def get(self, request):
        users = User.objects.all()
        return render(request, 'user_list.html', {'users': users})


@method_decorator(login_required(login_url='login_page'), name='dispatch')
class UserCreateView(View):
    def get(self, request):
        form = UserForm()
        return render(request, 'user_form.html', {'form': form})

    def post(self, request):
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user-list')
        return render(request, 'user_form.html', {'form': form})


@method_decorator(login_required(login_url='login_page'), name='dispatch')
class UserUpdateView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserForm(instance=user)
        return render(request, 'user_form.html', {'form': form})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user-list')
        return render(request, 'user_form.html', {'form': form})


@method_decorator(login_required(login_url='login_page'), name='dispatch')
class UserDeleteView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        return render(request, 'user_confirm_delete.html', {'user': user})

    def post(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        user.delete()
        return redirect('user-list')


@method_decorator(login_required(login_url='login_page'), name='dispatch')
class NotificationListView(View):
    def get(self, request):
        notifications = Notification.objects.filter(user=request.user)
        return render(request, 'notifications.html', {'notifications': notifications})

@method_decorator(login_required(login_url='login_page'), name='dispatch')
class KPIReportView(View):
    def get(self, request):
        tasks = Task.objects.filter(assigned_to=request.user)
        completed_tasks = tasks.filter(status='completed').count()
        overdue_tasks = tasks.filter(status='dead').count()
        in_progress_tasks = tasks.filter(status='not completed').count()

        context = {
            'total_tasks': tasks.count(),
            'completed_tasks': completed_tasks,
            'overdue_tasks': overdue_tasks,
            'in_progress_tasks': in_progress_tasks,
        }

        return render(request, 'kpi_report.html', context)


@method_decorator(login_required(login_url='login_page'), name='dispatch')
class StartPageView(TemplateView):
    template_name = 'start_page.html'