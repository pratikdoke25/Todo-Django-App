from rest_framework import viewsets, filters
from django.db.models import Case, When, Value, IntegerField

from .models import Todo, Category
from .serializers import TodoSerializer, CategorySerializer
from .pagination import CustomPagination


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TodoViewSet(viewsets.ModelViewSet):
    queryset = Todo.objects.all()
    serializer_class = TodoSerializer

    pagination_class = CustomPagination

    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter
    ]

    search_fields = ["title", "note"]
    ordering_fields = [
        "created_at",
        "due_date",
        "priority_rank"
    ]

    ordering = ["-created_at", "-id"]

    def get_queryset(self):
        queryset = super().get_queryset()

        queryset = queryset.annotate(
            priority_rank=Case(
                When(priority="LOW", then=Value(1)),
                When(priority="MEDIUM", then=Value(2)),
                When(priority="HIGH", then=Value(3)),
                default=Value(0),
                output_field=IntegerField()
            )
        )

        completed = self.request.query_params.get("completed")
        priority = self.request.query_params.get("priority")
        category = self.request.query_params.get("category")

        if completed is not None:
            if completed.lower() == "true":
                queryset = queryset.filter(completed=True)
            elif completed.lower() == "false":
                queryset = queryset.filter(completed=False)

        if priority:
            queryset = queryset.filter(priority=priority.upper())

        if category:
            queryset = queryset.filter(category_id=category)

        return queryset