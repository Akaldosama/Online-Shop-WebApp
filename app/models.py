from django.db import models

class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=10, unique=True)
    items = models.JSONField()  # Store items as JSON (e.g., [{"item": "Pizza", "qty": 1}])
    status = models.CharField(max_length=20, choices=[
        ("pending", "Pending"),
        ("preparing", "Preparing"),
        ("on_the_way", "On the way"),
        ("delivered", "Delivered")
    ], default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.order_number} - {self.user.name}"
