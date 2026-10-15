from rest_framework import serializers
from .models import Todo, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]
        read_only_fields = ["id"]

class TodoSerializer(serializers.ModelSerializer):
    is_overdue = serializers.BooleanField(read_only=True)

    class Meta:
        model = Todo
        fields = [
            "id",
            "title",
            "note",
            "completed",
            "priority",
            "due_date",
            "is_overdue",
            "created_at",
            "category"
        ]

        read_only_fields = [
            "id",
            "created_at",
            "is_overdue"
        ]