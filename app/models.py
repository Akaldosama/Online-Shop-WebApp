import random
import string

from django.db import models

class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    is_registered = models.BooleanField(default=False)
    # address = models.TextField()

    def __str__(self):
        return self.name

class Item(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()
    category = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

# class Order(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     order_number = models.CharField(max_length=10, unique=True)
#     items = models.JSONField()  # Store items as JSON (e.g., [{"item": "Pizza", "qty": 1}])
#     status = models.CharField(max_length=20, choices=[
#         ("pending", "Pending"),
#         ("preparing", "Preparing"),
#         ("on_the_way", "On the way"),
#         ("delivered", "Delivered")
#     ], default="pending")
#     created_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Order {self.order_number} - {self.user.name}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=10, unique=True)
    items = models.ManyToManyField(Item)  # Store items as a relationship instead of JSON
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("preparing", "Preparing"),
        ("on_the_way", "On the way"),
        ("delivered", "Delivered")
    ], default="pending")
    latitude = models.FloatField(null=True, blank=True)  # ✅ Store Latitude
    longitude = models.FloatField(null=True, blank=True)  # ✅ Store Longitude
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Order {self.order_number} - {self.user.name}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.item.title} (Order {self.order.order_number})"

