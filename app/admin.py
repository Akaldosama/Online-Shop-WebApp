from django.contrib import admin
from .models import Item, User, Order, OrderItem

# admin.site.register(Item)
@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'category', 'price')
admin.site.register(Order)
admin.site.register(User)
admin.site.register(OrderItem)
