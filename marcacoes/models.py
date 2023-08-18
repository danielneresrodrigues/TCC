from django.db import models
from geopy.geocoders import Nominatim
from django.contrib.auth.mixins import LoginRequiredMixin

from users.models import CustomUser

class Marcacoes(LoginRequiredMixin, models.Model):

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    data = models.DateTimeField()
    latitude = models.FloatField(default = 0)
    longitude = models.FloatField(default = 0)
    endereco = models.CharField(max_length = 250, null = True, blank = True)

    def __str__(self):
        
        return f'{self.user.first_name} {self.user.last_name} | {self.data}'
    
    def save(self, *args, **kwargs):

        geolocator = Nominatim(user_agent="my-app")

        self.endereco = geolocator.reverse((self.latitude, self.longitude))

        super().save(*args, **kwargs)