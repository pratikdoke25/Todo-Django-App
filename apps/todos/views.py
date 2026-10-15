from django.utils import timezone
from rest_framework import viewsets, filters ,status
from django.db.models import Case, When, Value, IntegerField

from .models import Todo, Category
from .serializers import TodoSerializer, CategorySerializer
from .pagination import CustomPagination


from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
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

        if self.action == "trash":
            queryset = queryset.filter(is_deleted = True)
        else :
            queryset = queryset.filter(is_deleted=False)


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
    
    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.deleted_at = timezone.now()

        instance.save(
            update_fields=["is_deleted", "deleted_at"]
        )

    # Get all deleted todos
    @action(detail=False, methods=["get"])
    def trash(self, request):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    # Restore deleted todo
    @action(detail=True, methods=["post"])
    def restore(self, request, pk=None):
        todo = Todo.objects.filter(
            pk=pk,
            is_deleted=True
        ).first()

        if todo is None:
            raise NotFound("Deleted todo not found.")

        todo.is_deleted = False
        todo.deleted_at = None

        todo.save(
            update_fields=["is_deleted", "deleted_at"]
        )

        return Response(
            {
                "message": "Todo restored successfully"
            },
            status=status.HTTP_200_OK
        )

    # Permanently delete todo
    @action(
        detail=True,
        methods=["delete"],
        url_path="permanent-delete"
    )
    def permanent_delete(self, request, pk=None):
        todo = Todo.objects.filter(
            pk=pk,
            is_deleted=True
        ).first()

        if todo is None:
            raise NotFound("Deleted todo not found.")

        todo.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )