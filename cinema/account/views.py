from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from django.contrib.auth import logout
from .forms import LoginForm, UserRegistrationForm


def logout_view(request):
    logout(request)
    return redirect('/')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print('password is ', cd['password'])
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/')
                else:
                    error = 'Доступ запрещен!'
                    return render(request, 'account/login.html', {'form': form, 'error': error})
            else:
                error = 'Неправильный пароль или пользователь!'
                return render(request, 'account/login.html', {'form': form, 'error': error})
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            if len(str(user_form.cleaned_data['password'])) >= 6:
                print('password is =', user_form.cleaned_data['password'])
                new_user = user_form.save(commit=False)
                new_user.set_password(user_form.cleaned_data['password'])
                new_user.save()
                return render(request, 'account/register_done.html', {'new_user': new_user})
            else:
                error = 'Длина пароля должна быть больше 6 символов'
                return render(request, 'account/register.html', {'user_form': user_form, 'error': error})
        else:
            error = 'Ошибка заполнения данных'
            return render(request, 'account/register.html', {'user_form': user_form, 'error': error})

    else:
        user_form = UserRegistrationForm()

    return render(request, 'account/register.html', {'user_form': user_form})