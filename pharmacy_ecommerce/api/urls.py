from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'profiles', views.UserProfileViewSet)
router.register(r'products', views.ProductViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'orders', views.OrderViewSet, basename='order')
router.register(r'order-items', views.OrderItemViewSet, basename='orderitem')
router.register(r'cart', views.CartViewSet, basename='cart')
router.register(r'cart-items', views.CartItemViewSet, basename='cartitem')
router.register(r'prescriptions', views.PrescriptionViewSet, basename='prescription')
router.register(r'coupons', views.CouponViewSet, basename='coupon')
router.register(r'wishlist', views.WishlistViewSet, basename='wishlist')
router.register(r'stock-notifications', views.StockNotificationViewSet, basename='stocknotification')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
