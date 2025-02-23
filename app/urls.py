from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, OrderViewSet, ItemViewSet, order_list_view

# URL Routing
router = DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'items', ItemViewSet, basename='items')

urlpatterns = [
    path('api/', include(router.urls)),
    path('items/', order_list_view, name='items_page'),
    path('api/orders/create-order/', OrderViewSet.as_view({'post': 'create_order'}), name='create_order'),
    # New endpoint
]
