from datetime import timezone
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Todo(models.Model) :

    class Priority(models.TextChoices):
        LOW = "LOW", "Low"
        MEDIUM = "MEDIUM", "Medium"
        HIGH = "HIGH", "High"


    title =  models.CharField(max_length=200)
    note = models.CharField(max_length=500)
    completed = models.BooleanField(default=False)

    priority = models.CharField(
        max_length=10,
        choices=Priority.choices,
        default=Priority.MEDIUM
    )

    due_date = models.DateTimeField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)


    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="todos",
        null=True,
        blank=True
    )

    is_deleted = models.BooleanField(default=False)

    deleted_at  = models.DateTimeField(null=True,
                                       blank=True)

    @property
    def is_overdue(self):
        return (
            not self.completed
            and self.due_date is not None
            and self.due_date < timezone.now()
        )

    def __str__(self):
        return self.title