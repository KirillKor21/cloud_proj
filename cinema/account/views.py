from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import LoginForm, UserRegistrationForm
from datetime import datetime, timedelta, timezone
from . import models



def logout_view(request):
    logout(request)
    return redirect('/')


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print('password is ', cd['password'])

            # защита от брудфорса
            # Проверка на существования пользователя
            if models.BlockedUsers.objects.filter(user=str(cd['username'])).exists():
                def_user = models.BlockedUsers.objects.get(user=str(cd['username']))
                # Установка текущего времени
                current_datetime = datetime.now(timezone.utc) + timedelta(hours=3)

                print("current_datetime is ", current_datetime)
                print("type of current_datetime is ", type(current_datetime))
                print("def_user.time is ", def_user.time)
                print('type of datetime(def_user.time) is ', type(def_user.time))

                print("---------------------------")

                print("current_datetime - timedelta(minutes=3) is ", current_datetime - timedelta(minutes=3))
                print("def_user.time is ", current_datetime - def_user.time)

                # Сравнение текущего времени и последней попытка
                if (current_datetime - def_user.time > timedelta(minutes=3)):
                    def_user.count = 0
                else:
                    def_user.count = def_user.count + 1

                # Сохранение данных
                def_user.time = current_datetime
                def_user.save()

                user = authenticate(username=cd['username'], password=cd['password'])
                # В случае если попыток было меньше трех
                if def_user.count < 3:
                    if user is not None:
                        if user.is_active:
                            #Обнуление при удачном входе
                            def_user.count = 0
                            def_user.save()
                            login(request, user)
                            return redirect('/')
                        else:
                            error = 'Доступ запрещен!'
                            return render(request, 'account/login.html', {'form': form, 'error': error})
                    else:
                        error = 'Неправильный пароль или пользователь!'
                        return render(request, 'account/login.html', {'form': form, 'error': error})
                # Если попыток больше чем 3, то блокировка на 3 минуты
                else:
                    error = 'Слишком много попыток! Аккаунт заблокирован на 3 минуты '
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

                user_def = models.BlockedUsers(user=new_user.username, count=0)
                user_def.time = datetime.now()
                user_def.save()

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
