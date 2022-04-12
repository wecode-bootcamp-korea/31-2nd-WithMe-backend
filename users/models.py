from django.db import models
from cores.models   import TimestampZone

class User(TimestampZone):
    nickname = models.CharField(max_length=45)
    email = models.CharField(max_length=100)
    social_id = models.IntegerField()
    profile_image = models.CharField(max_length=1000)
    description = models.TextField(null=True)
    point = models.DecimalField(decimal_places=2, max_digits=10)
    host = models.ForeignKey('Host', on_delete=models.CASCADE)

    class Meta:
        db_table = 'users'

class Host(TimestampZone):
    bank = models.CharField(max_length=45)
    account = models.CharField(max_length=45)
    registration = models.CharField(max_length=45)

    class Meta:
        db_table = 'hosts'
    