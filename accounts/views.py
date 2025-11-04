from rest_framework import status, viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from destinations.models import Destination
from bookings.models import Booking

User = get_user_model()


# ----------------------
# Public Auth APIs
# ----------------------
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Public access

    def post(self, request):
        username = request.data.get("username")
        email = request.data.get("email")
        password = request.data.get("password")
        role = request.data.get("role", "user")  # default to 'user'

        if not username or not password or not email:
            return Response({"error": "All fields are required"}, status=status.HTTP_400_BAD_REQUEST)

        # Validate role
        allowed_roles = [choice[0] for choice in getattr(User, "ROLE_CHOICES", [])]
        if role not in allowed_roles:
            return Response({"error": f"Invalid role. Allowed roles: {allowed_roles}"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, email=email, password=password, role=role)
        user.save()

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Registration successful ✅",
            "user": {
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = [AllowAny]  # Public access

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response({"error": "Both username and password are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        refresh = RefreshToken.for_user(user)

        return Response({
            "message": "Login successful ✅",
            "user": {
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)
# ----------------------
# Admin User Management
# ----------------------
class AdminUserViewSet(viewsets.ViewSet):
    """
    Admin-only viewset to manage users
    """
    permission_classes = [permissions.IsAuthenticated]  # Must be authenticated

    def get_permissions(self):
        # Only users with role 'admin' and not banned can access
        if not (self.request.user.is_authenticated and self.request.user.role == "admin"):
            self.permission_denied(
                self.request, message="You must be an admin to access this endpoint."
            )
        return super().get_permissions()

    @action(detail=False, methods=["get"])
    def list_users(self, request):
        """
        List all users with their role and status
        """
        users = User.objects.all().values("id", "username", "email", "role", "is_active")
        return Response(users)

    @action(detail=True, methods=["post"])
    def ban(self, request, pk=None):
        """
        Ban a user (set is_active=False) except admin
        """
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
        """
        Unban a user (set is_active=True)
        """
        try:
            user = User.objects.get(pk=pk)
            user.is_active = True
            user.save()
            return Response({"message": f"User {user.username} has been unbanned"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=["get"])
    def stats(self, request):
        """
        Show stats: total destinations, packages, bookings
        """
        total_destinations = Destination.objects.count()
        total_packages = Package.objects.count()
        total_bookings = Booking.objects.count()

        return Response({
            "total_destinations": total_destinations,
            "total_packages": total_packages,
            "total_bookings": total_bookings
        })