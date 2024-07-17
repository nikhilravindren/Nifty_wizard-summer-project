from django.contrib import admin
from .models import stocks,fundamental,predictors,messages
# Register your models here.
admin.site.register(stocks)
admin.site.register(fundamental)
admin.site.register(predictors)
admin.site.register(messages)