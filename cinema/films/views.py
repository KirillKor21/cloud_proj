from django.shortcuts import render, redirect
from django.urls import reverse
from . import models
import requests


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
                    print("Can't find it in search")
            try:
                print("name_film ===", name_films)
                Film = models.Film.objects.get(name=name_films)
                print ("Film===", Film )
                context = {'Film': Film}
                return render(request, "films/this_film.html", context=context)
            except:
                print("Can't find it")
                
    all_films = models.Film.objects.all()
    for Film in all_films:
        print('Poster is ', Film.poster)
        name_file = str(Film.poster)
        url = 'https://storage.yandexcloud.net/my-backet-kku201-331/' + name_file
        print('url is ', url)

        req = requests.get(url)
        path = '/home/kku201-331/cloud_proj/cinema/media/posters/'
        file = open(path + name_file, "wb")
        file.write(req.content)
        file.close()
    
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
            id = int(request.POST['id'])
            all_films = models.Film.objects.all()
            for Film in all_films:
                if Film.id == id:
                    film = Film.name
            name = request.POST['name']
            msg = request.POST['msg']
            stars = request.POST['stars']
            models.Review.objects.create(name=name, film=film, msg=msg, stars=stars)
            return redirect(reverse('films:reviews'))
        else:
            all_films = models.Film.objects.all()
            film_id = request.GET.get("films", 0)
            context = context = {'film_id': int(film_id), "all_films": all_films}
            return render(request, 'films/add_review.html', context=context)


def add(request):
    UPLOAD_FOLDER = './static/films'
    ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}
    if request.POST:

        name = request.POST.get('name')
        studio = request.POST.get('studio')
        time = request.POST.get('time')
        room_number = request.POST.get('room_number')
        stars = request.POST.get('stars')
        trailer = request.POST.get('trailer')
        description = request.POST.get('description')
        poster = request.FILES.get("poster")
        poster_url = 'films/' + str(poster)

        th_film = models.Film(
            name=name, studio=studio, time=time, room_number=room_number, poster=poster, stars=stars, poster_url=poster_url, description=description, trailer=trailer
        )
        
        th_film.save()
        
        path = '/home/kku201-331/cloud_proj/cinema/media/posters/'
        name_file = str(poster)
        url = 'https://storage.yandexcloud.net/my-backet-kku201-331/' + name_file
        print('url is ', url)
        file = open(path + name_file, 'rb')

        req = requests.put(url, file)

        file.close()
        print('Mes of file upload is ', req.text)
        
        
        return redirect(reverse('films:list'))
    else:
        return render(request, 'films/add.html')


def delete(request):
    if request.POST:
        id=request.POST['id']
        try:
            models.Film.objects.get(pk=id).delete()
            return redirect(reverse('films:list'))
        except:
            print('pk not found')
    else:
        all_films = models.Film.objects.all()
        film_id = request.GET.get("films", 0)
        context = context = {'film_id': int(film_id), "all_films": all_films}
        return render(request, 'films/delete.html', context=context)


def list(request):
    all_films = models.Film.objects.all()
    context = {'all_films': all_films}
    return render(request, 'films/list.html', context=context)
