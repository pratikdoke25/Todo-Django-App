# config/views.py

from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema


class HealthResponseSerializer(serializers.Serializer):
    message = serializers.CharField()


@extend_schema(
    summary="Check API status",
    responses=HealthResponseSerializer,
    tags=["Health"],
)
@api_view(["GET"])
def health_check(request):
    return Response({"message": "API is working!"})