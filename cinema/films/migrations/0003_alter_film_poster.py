# Generated by Django 4.2.1 on 2023-05-29 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0002_film_poster_url_alter_film_poster'),
    ]

    operations = [
        migrations.AlterField(
            model_name='film',
            name='poster',
            field=models.FileField(null=True, upload_to='films/static/films/'),
        ),
    ]