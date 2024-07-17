from django.db import models
from django.contrib.auth.models import User
import datetime

# Create your models here.

class stocks(models.Model):
        name = models.CharField(max_length=100, null=False, blank=False)
        symbol = models.CharField(max_length=100, null=False, blank=False)
        sector = models.CharField(max_length=100, null=False, blank=False,default=1)
        description = models.TextField(max_length=1000, null=False, blank=False,default=1)

class fundamental(models.Model):
        stock = models.ForeignKey(stocks, on_delete=models.CASCADE)
        eps = models.FloatField(null=False, blank=False)
        market_cap = models.BigIntegerField(null=False, blank=False)
        roe = models.FloatField(null=False, blank=False)
        debt = models.FloatField(null=False, blank=False)
        pe_ratio = models.FloatField(null=False, blank=False)
        pb_ratio = models.FloatField(null=False, blank=False)
        divident = models.FloatField(null=False, blank=False)
        book_value = models.FloatField(null=False, blank=False)
        face_value = models.FloatField(null=False, blank=False)


class predictors(models.Model):
        stock = models.ForeignKey(stocks, on_delete=models.CASCADE)
        model = models.FileField(upload_to='predictors/')
        scalar = models.FileField(upload_to='predictors/')

class messages(models.Model):
        user = models.ForeignKey(User,on_delete=models.CASCADE)
        models.DateTimeField(default=datetime.datetime.now)
        msg = models.CharField(max_length=225)


