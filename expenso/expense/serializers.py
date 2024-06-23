from rest_framework import serializers

from .models import Category, Expense


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializer for Category model.
    """

    class Meta:
        model = Category
        fields = "__all__"


class ExpenseSerializer(serializers.ModelSerializer):
    """
    Serializer for Expense model.
    """

    category_obj = CategorySerializer(source="category", read_only=True)

    class Meta:
        model = Expense
        fields = "__all__"
        extra_kwargs = {
            "name": {"required": True},
            "amount": {"required": True},
            "category": {"required": True},
            "date": {"required": False},
            "user": {"read_only": True},
        }

    def validate_amount(self, value):
        if value <= 0:
            raise serializers.ValidationError("Amount must be positive.")
        return value
