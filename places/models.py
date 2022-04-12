from datetime import datetime
from django.db import models
from users.models  import User,Host
from cores.models   import TimestampZone

class Place(TimestampZone):
    title = models.CharField(max_length=45)
    subtitle = models.CharField(max_length=45)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    running_time = models.IntegerField()
    running_date = models.DateField()
    location = models.CharField(max_length=45)
    preparation = models.CharField(max_length=45)
    max_visitor = models.IntegerField()
    image_url = models.CharField(max_length=1000)
    host = models.ForeignKey( Host , on_delete=models.CASCADE)
    close_date = models.DateField()
    status = models.ForeignKey('status' , on_delete=models.CASCADE)

    class Meta:
        db_table = 'places'

class Status(TimestampZone):
    status = models.BooleanField(default=False)

    class Meta:
        db_table = 'statuses'

class Reservation(TimestampZone):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey('Place', on_delete=models.CASCADE)

    class Meta:
        db_table = 'reservations'

class Review(TimestampZone):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place = models.ForeignKey('Place', on_delete=models.CASCADE)
    review = models.TextField()

    class Meta:
        db_table = 'reviews'    



