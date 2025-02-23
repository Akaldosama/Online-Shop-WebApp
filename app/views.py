import json

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.crypto import get_random_string
from .models import User, Order, Item, OrderItem
from .serializers import UserSerializer, OrderSerializer, ItemSerializer

# User ViewSet
# class UserViewSet(viewsets.ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#     def create(self, request, *args, **kwargs):
#         telegram_id = request.data.get('telegram_id')
#         name = request.data.get('name', 'Unknown')
#         phone = request.data.get('phone', '')
#
#         user, created = User.objects.get_or_create(telegram_id=telegram_id, defaults={'name': name, 'phone': phone})
#
#         serializer = self.get_serializer(user)
#         return Response(serializer.data, status=201 if created else 200)


class UserViewSet(viewsets.ModelViewSet):
    """Handles user registration via Telegram ID."""

    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        """Registers a user via Telegram ID."""
        data = request.data
        telegram_id = data.get('telegram_id')
        name = data.get('name')
        phone = data.get('phone')

        if not telegram_id or not name or not phone:
            return Response({'error': 'Telegram ID, name, and phone are required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Find or create user by telegram_id
        user, created = User.objects.get_or_create(telegram_id=telegram_id)

        if not created and user.is_registered:
            return Response({
                'message': 'User is already registered.',
                'name': user.name,
                'phone': user.phone,
            }, status=status.HTTP_200_OK)

        # Update user information and mark as registered
        user.name = name
        user.phone = phone
        user.is_registered = True
        user.save()

        return Response({
            'message': 'User registered successfully.',
            'name': user.name,
            'phone': user.phone,
        }, status=status.HTTP_201_CREATED)


# Order ViewSet
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    @action(detail=False, methods=['post'])
    def create_order(self, request):
        data = request.data
        telegram_id = data.get('telegram_id')
        cart_items = data.get('cart')

        if not telegram_id or not cart_items:
            return Response({'error': 'Telegram ID and cart items are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Find or create user
        user, _ = User.objects.get_or_create(telegram_id=telegram_id)

        # Create Order
        order = Order.objects.create(user=user)

        # Add Items to Order
        for item_id, details in cart_items.items():
            item = Item.objects.get(id=item_id)
            OrderItem.objects.create(order=order, item=item, quantity=details['quantity'])

        return Response({'message': 'Order created successfully', 'order_number': order.order_number}, status=status.HTTP_201_CREATED)

# Item ViewSet
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

# Frontend Order List View
def order_list_view(request):
    items = Item.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'items': items})
