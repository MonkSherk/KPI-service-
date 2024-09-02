from django.shortcuts import redirect


def RSRequired(func):
    def wrapper(request, *args, **kwargs):
        if request.user.role.name == 'Руководитель':
            return func(request, *args, **kwargs)
        else:
            return redirect('start_page')
    return wrapper
