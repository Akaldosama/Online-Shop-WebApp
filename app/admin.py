from django.contrib import admin
from .models import Item, User, Order

admin.site.register(Order)
admin.site.register(Item)
admin.site.register(User)
