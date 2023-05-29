from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

class Film(models.Model):
    name = models.CharField(max_length=50)
    studio = models.CharField(max_length=50)
    time = models.TimeField()
    room_number = models.IntegerField()
    poster = models.FileField(upload_to='films/static/films')
    poster_url = models.CharField(max_length=50)
    stars = models.IntegerField()

    def __str__(self):
        return f"Film is {self.name} by {self.studio} at {self.time} in {self.room_number}, rating: {self.stars}, path {self.poster}"

class Review(models.Model):
    name = models.CharField(max_length=50)
    film = models.CharField(max_length=50)
    msg = models.CharField(max_length=200)
    stars = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)])

    def __str__(self):
        return f"Review is {self.name} by {self.film} is: {self.msg}, stars:"

