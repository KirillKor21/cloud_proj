from django.contrib import admin
from films.models import Film
from films.models import Review


class FilmAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Film name', {'fields': ['name']}),
        ('Film studio', {'fields': ['studio']}),
        ('Show time', {'fields': ['time']}),
        ('Room number', {'fields': ['room_number']}),
        ('Poster', {'fields': ['poster']}),
        ('Stars', {'fields': ['stars']})
    ]

admin.site.register(Film, FilmAdmin)

class ReviewAdmin(admin.ModelAdmin):
    fieldsets = [
        ('Username', {'fields': ['name']}),
        ('Film', {'fields': ['film']}),
        ('Message', {'fields': ['msg']}),
        ('Stars', {'fields': ['stars']})
    ]
admin.site.register(Review, ReviewAdmin)
