from core.models import TimeStampedModel
from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

User = get_user_model()


class Category(TimeStampedModel):
    """
    Model for storing categories.
    Can only be added/modified by the admin.
    """

    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Expense(TimeStampedModel):
    """
    Model for storing expenses.
    """

    name = models.CharField(max_length=255)
    notes = models.TextField(blank=True, null=True)
    amount = models.IntegerField(null=False, blank=False)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name="expenses",
        null=True,
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="expenses")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name
