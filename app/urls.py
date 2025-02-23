from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, OrderViewSet, ItemViewSet, order_list_view

# URL Routing
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'orders', OrderViewSet)
router.register(r'items', ItemViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('items/', order_list_view, name='items_page'),
]
