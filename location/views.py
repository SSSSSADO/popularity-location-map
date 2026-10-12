from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import filters, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from .models import Category, Location
from .permissions import IsAuthorOrAdminOrReadOnly
from .serializers import CategorySerializer, CategoryListSerializer, LocationSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return CategoryListSerializer
        return CategorySerializer


class LocationViewSet(viewsets.ModelViewSet):
    serializer_class = LocationSerializer
    permission_classes = [IsAuthorOrAdminOrReadOnly]
    filter_backends = [
            DjangoFilterBackend,
            filters.SearchFilter,
            filters.OrderingFilter,
    ]
    filterset_fields = ["category", "author"]
    search_fields = ["name", "description"]
    ordering_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        return (
            Location.objects
            .filter(is_deleted=False)
            .select_related("category", "author")
        )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])
