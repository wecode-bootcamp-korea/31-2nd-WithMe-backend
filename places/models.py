from django.db      import models
from cores.models   import TimestampZone


class Place(TimestampZone):
    title        = models.CharField(max_length=45)
    subtitle     = models.CharField(max_length=200)
    price        = models.DecimalField(decimal_places=2, max_digits=10)
    running_time = models.IntegerField()
    running_date = models.DateField()
    location     = models.CharField(max_length=45)
    preparation  = models.CharField(max_length=45)
    max_visitor  = models.IntegerField()
    image_url    = models.CharField(max_length=1000)
    close_date   = models.DateField()
    latitude     = models.DecimalField(max_digits=18,decimal_places=10)
    longitude    = models.DecimalField(max_digits=18,decimal_places=10)
    status       = models.ForeignKey('Placestatus', on_delete=models.CASCADE)
    host         = models.ForeignKey('users.Host', on_delete=models.CASCADE)

    class Meta:
        db_table = 'places'

class PlaceStatus(models.Model):
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'place_statuses'

class Reservation(TimestampZone):
    user  = models.ForeignKey('users.User', on_delete=models.CASCADE)
    place = models.ForeignKey('Place', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reservations'

class Review(TimestampZone):
    user   = models.ForeignKey('users.User', on_delete=models.CASCADE)
    place  = models.ForeignKey('Place', on_delete=models.CASCADE)
    content = models.TextField()

    class Meta:
        db_table = 'reviews'