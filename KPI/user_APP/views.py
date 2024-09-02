
# Create your views here.
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from user_APP.forms import SignUp, SignIn


# Create your views here.
def register_view(request):
    if request.user.is_authenticated:
        return redirect('start_page')
    form = SignUp()
    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('start_page')
    ctx = {'form': form}
    return render(request, 'user_APP/register.html', context=ctx)


def login_view(request):
    if request.user.is_authenticated:
        return redirect('start-page')
    form = SignIn()
    if request.method == 'POST':
        form = SignIn(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            print(user)
            print(username)
            print(password)
            if user is not None:
                login(request, user)
                return redirect('user-list')
    ctx = {'form': form}
    return render(request, 'user_APP/login.html', context=ctx)


@login_required(login_url='login_page')
def logout_view(request):
    logout(request)
    return redirect('login_page')
