from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import CategoryListAPIView, ExpenseAPIViewSet

app_name = "expense"

expense_router = DefaultRouter()
expense_router.register(r"", ExpenseAPIViewSet, basename="expense")

urlpatterns = [
    path("category/", CategoryListAPIView.as_view(), name="category-list"),
]

urlpatterns += expense_router.urls
