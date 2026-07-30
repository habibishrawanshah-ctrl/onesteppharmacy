from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import (
    ProductSerializer, CategorySerializer, OrderSerializer, OrderItemSerializer,
    CartSerializer, CartItemSerializer, PrescriptionSerializer, CouponSerializer,
    WishlistSerializer, StockNotificationSerializer, UserSerializer, UserProfileSerializer,
)
from products.models import Product, Category, Wishlist, StockNotification
from orders.models import Order, OrderItem, Cart, CartItem, Prescription, Coupon
from django.contrib.auth.models import User
from users.models import UserProfile


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAdminUser]


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.select_related('category').all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'is_prescription_required']
    search_fields = ['name', 'description', 'generic_name']
    ordering_fields = ['price', 'name', 'created_at']


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_at']

    def get_queryset(self):
        qs = Order.objects.prefetch_related('items__product').all()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs


class OrderItemViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = OrderItem.objects.select_related('product', 'order').all()
        if not self.request.user.is_staff:
            qs = qs.filter(order__user=self.request.user)
        return qs


class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user).prefetch_related('items__product')


class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user).select_related('product')


class PrescriptionViewSet(viewsets.ModelViewSet):
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['status']

    def get_queryset(self):
        qs = Prescription.objects.all()
        if not self.request.user.is_staff:
            qs = qs.filter(user=self.request.user)
        return qs


class CouponViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coupon.objects.filter(is_active=True)
    serializer_class = CouponSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['code']


class WishlistViewSet(viewsets.ModelViewSet):
    serializer_class = WishlistSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.filter(user=self.request.user).select_related('product')


class StockNotificationViewSet(viewsets.ModelViewSet):
    serializer_class = StockNotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return StockNotification.objects.filter(user=self.request.user)
