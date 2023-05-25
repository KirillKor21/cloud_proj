from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic.edit import CreateView

from . import models


def films_view(request):
    if request.POST:
        try:
            sorts = request.POST["sort"]
            all_films = models.Film.objects.all().order_by(sorts)
            context = {'all_films': all_films}
            return render(request, 'films/films_view.html', context=context)
        except:
            try:
                name_films = request.POST["Name_film"]
            except:
                try:
                    name_films = request.POST["search"]
                except:
                    print("Can't find it")
            try:
                Film = models.Film.objects.get(name=name_films)
                context = {'Film': Film}
                return render(request, "films/this_film.html", context=context)
            except:
                print("Can't find it")
    all_films = models.Film.objects.all()
    print(all_films)
    context = {'all_films': all_films}
    return render(request, 'films/films_view.html', context=context)

def mainpage(request):
    if request.POST:
        try:
            name_films = request.POST["search"]
            Film = models.Film.objects.get(name=name_films)
            context = {'Film': Film}
            return render(request, "films/this_film.html", context=context)
        except:
            print("Can't find it")
    return render(request, 'films/mainpage.html')

def reviews(request):
    all_reviews = models.Review.objects.all()
    context = {'all_reviews': all_reviews}
    return render(request, 'films/reviews.html', context=context)

def add_review(request):
        if request.POST:
            name = request.POST['name']
            film = request.POST['film']
            msg = request.POST['msg']
            stars = request.POST['stars']
            models.Review.objects.create(name=name, film=film, msg=msg, stars=stars)
            return redirect(reverse('films:reviews'))
        else:
            return render(request, 'films/add_review.html')


def add(request):
    if request.POST:
        name = request.POST['name']
        studio = request.POST['studio']
        time = request.POST['time']
        room_number = request.POST['room_number']
        poster = request.POST['poster']
        stars = request.POST['stars']
        models.Film.objects.create(name=name, studio=studio, time=time, room_number=room_number, poster=poster, stars=stars)
        return redirect(reverse('films:list'))
    else:
        return render(request, 'films/add.html')

def delete(request):
    if request.POST:
        pk=request.POST['pk']
        try:
            models.Film.objects.get(pk=pk).delete()
            return redirect(reverse('films:list'))
        except:
            print('pk not found')
    else:
        return render(request, 'films/delete.html')

def list(request):
    all_films = models.Film.objects.all()
    context = {'all_films': all_films}
    return render(request, 'films/list.html', context=context)


class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"