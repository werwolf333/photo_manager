from django.contrib.auth.models import User
from django.db import models


class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.CharField(blank=True, null=True, max_length=200)
    geo_longitude = models.FloatField(blank=True, null=True, max_length=200)
    geo_latitude = models.FloatField(blank=True, null=True, max_length=200)
    geo_altitude = models.FloatField(blank=True, null=True, max_length=200)
    date_of_download = models.DateTimeField(auto_now=True)
    image = models.ImageField(blank=True, upload_to='images/core/', help_text='100x100px',
                              verbose_name='ссылка картинки')


class Person (models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    photo = models.ForeignKey(Photo, related_name='human', on_delete=models.DO_NOTHING)
