from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Destination, Package
from .serializers import DestinationSerializer, PackageSerializer
from .permissions import IsAgentOrAdminOrReadOnly

# ----------------------
# Destination ViewSet
# ----------------------
class DestinationViewSet(viewsets.ModelViewSet):
    queryset = Destination.objects.all()
    serializer_class = DestinationSerializer
    permission_classes = [IsAgentOrAdminOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the creator
        serializer.save(created_by=self.request.user)


# ----------------------
# Package ViewSet
# ----------------------
class PackageViewSet(viewsets.ModelViewSet):
    queryset = Package.objects.all()
    serializer_class = PackageSerializer
    permission_classes = [IsAgentOrAdminOrReadOnly]

    def perform_create(self, serializer):
        # Automatically set the creator
        serializer.save(created_by=self.request.user)

    @action(detail=True, methods=["post"], permission_classes=[permissions.IsAuthenticated])
    def like(self, request, pk=None):
        """
        Toggle like/unlike on a package.
        """
        package = self.get_object()
        user = request.user

        if user in package.likes.all():
            package.likes.remove(user)
            message = "Unliked the package"
        else:
            package.likes.add(user)
            message = "Liked the package"

        # Return message and current like count
        return Response(
            {"message": message, "likes_count": package.likes.count()},
            status=status.HTTP_200_OK
        )
