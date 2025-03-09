from django.contrib import admin
from .models import Card, CardRequest, CardFile, MyHolder
# Register your models here.

admin.site.register(CardFile)
admin.site.register(Card)
admin.site.register(CardRequest)
admin.site.register(MyHolder)