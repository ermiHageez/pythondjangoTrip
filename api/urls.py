# api/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from destinations.views import DestinationViewSet, PackageViewSet
from bookings.views import BookingViewSet
from accounts.views import RegisterView, LoginView
from accounts.admin_views import AdminUserViewSet  # your admin viewset

router = DefaultRouter()
router.register(r"destinations", DestinationViewSet, basename="destinations")
router.register(r"packages", PackageViewSet, basename="packages")
router.register(r"bookings", BookingViewSet, basename="bookings")
router.register(r"admin/users", AdminUserViewSet, basename="admin-users")  # unique basename


urlpatterns = [
    # Auth endpoints
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),

    # API routes for CRUD
    path("", include(router.urls)),
]
