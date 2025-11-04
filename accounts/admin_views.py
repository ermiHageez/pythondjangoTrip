from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from destinations.models import Destination, Package
from bookings.models import Booking
from .permissions import IsAdminRole  # <- import the custom permission

User = get_user_model()

class AdminUserViewSet(viewsets.ViewSet):
    """
    Admin-only viewset to manage users
    """
    permission_classes = [IsAdminRole]  # Only users with role='admin'

    @action(detail=False, methods=["get"])
    def list_users(self, request):
        users = User.objects.all().values("id", "username", "email", "role", "is_active")
        return Response(users)

    @action(detail=True, methods=["post"])
    def ban(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            if user.role == "admin":
                return Response({"error": "Cannot ban an admin"}, status=status.HTTP_403_FORBIDDEN)
            user.is_active = False
            user.save()
            return Response({"message": f"User {user.username} has been banned"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=["post"])
    def unban(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            user.is_active = True
            user.save()
            return Response({"message": f"User {user.username} has been unbanned"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["get"])
    def stats(self, request):
        return Response({
            "total_destinations": Destination.objects.count(),
            "total_packages": Package.objects.count(),
            "total_bookings": Booking.objects.count()
        })
