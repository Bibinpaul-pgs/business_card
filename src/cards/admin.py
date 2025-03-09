from django.contrib import admin
from .models import Card, CardRequest, CardFile
# Register your models here.

admin.site.register(CardFile)
admin.site.register(Card)
admin.site.register(CardRequest)