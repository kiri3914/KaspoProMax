from django.contrib import admin
from .models import Currency, Profile, Card, Transaction


admin.site.register(Currency)
admin.site.register(Profile)
admin.site.register(Card)
admin.site.register(Transaction)
