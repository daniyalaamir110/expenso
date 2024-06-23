import datetime

from core.paginators import CustomPageNumberPagination
from django.db import models
from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from .models import Category, Expense
from .serializers import CategorySerializer, ExpenseSerializer


class CategoryListAPIView(ListAPIView):
    """
    View for listing categories.
    """

    serializer_class = CategorySerializer
    queryset = Category.objects.all().order_by("name")
    filter_backends = [SearchFilter]
    search_fields = ["name"]


class ExpenseAPIViewSet(ModelViewSet):
    """
    ViewSet for Expense model.
    """

    serializer_class = ExpenseSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    http_method_names = ["get", "post", "patch", "delete"]

    def get_queryset(self):
        user = self.request.user
        start_date = self.request.GET.get("start_date")
        end_date = self.request.GET.get("end_date")
        queryset = Expense.objects.filter(user_id=user.id)
        category_id = self.request.GET.get("category_id")
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="start_date",
                type=datetime.date,
            ),
            OpenApiParameter(
                name="end_date",
                type=datetime.date,
            ),
            OpenApiParameter(
                name="category_id",
                type=int,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data["total_amount"] = self.get_queryset().aggregate(
            total_amount=models.Sum("amount", default=0)
        )["total_amount"]
        return response

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        return super().perform_create(serializer)
