from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Booking
from .serializers import BookingSerializer
from destinations.models import Package
from django.contrib.auth import get_user_model

User = get_user_model()


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Only the owner of a booking or admin can edit/view.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return obj.user == request.user or request.user.is_staff
        return obj.user == request.user or request.user.is_staff


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        package = serializer.validated_data["package"]
        seats_requested = serializer.validated_data.get("seats", 1)

        # Check if seats are available
        if seats_requested > package.seats_remaining:
            return Response(
                {"error": "Not enough seats available"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Deduct seats
        package.seats_remaining -= seats_requested
        package.save()

        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Users see only their bookings, admins see all
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(user=user)

    @action(detail=False, methods=["get"])
    def my_bookings(self, request):
        user = request.user
        bookings = Booking.objects.filter(user=user)
        serializer = self.get_serializer(bookings, many=True)
        return Response(serializer.data)
