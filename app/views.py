from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.utils.crypto import get_random_string
from .models import User, Order, Item
from .serializers import UserSerializer, OrderSerializer, ItemSerializer

# User ViewSet
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        telegram_id = request.data.get('telegram_id')
        name = request.data.get('name', 'Unknown')
        phone = request.data.get('phone', '')

        user, created = User.objects.get_or_create(telegram_id=telegram_id, defaults={'name': name, 'phone': phone})

        serializer = self.get_serializer(user)
        return Response(serializer.data, status=201 if created else 200)

# Order ViewSet
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('-created_at')
    serializer_class = OrderSerializer

    @action(detail=False, methods=['post'])
    def create_order(self, request):
        telegram_id = request.data.get('telegram_id')
        items = request.data.get('items')

        if not telegram_id or not items:
            return Response({'error': 'Missing required fields'}, status=400)

        user, _ = User.objects.get_or_create(telegram_id=telegram_id)
        order_number = get_random_string(10).upper()
        order = Order.objects.create(user=user, order_number=order_number)
        order.items.set(Item.objects.filter(id__in=items))

        return Response({'message': 'Order created', 'order_number': order.order_number}, status=201)

# Item ViewSet
class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

# Frontend Order List View
def order_list_view(request):
    items = Item.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'items': items})
