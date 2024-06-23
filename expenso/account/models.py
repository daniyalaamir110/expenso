from core.models import TimeStampedModel
from django.contrib.auth.models import AbstractUser

from django.db import models
from django.utils import timezone


class RegistrationMethod(models.TextChoices):
    EMAIL = "EM", "Email"
    GOOGLE = "GO", "Google"


class User(AbstractUser):
    """
    This model extends the default Django user model.
    """

    email = models.EmailField(unique=True, blank=False, null=False)
    registration_method = models.CharField(
        choices=RegistrationMethod.choices,
        default=RegistrationMethod.EMAIL,
        max_length=2,
    )

    def __str__(self):
        return self.username


EMAIL_TOKEN_VALIDITY = 1


class UserEmailStatus(TimeStampedModel):
    """
    This model stores the user email status.
    Initially, it only contains the user field, which is a one-to-one
    field to the default Django user model.
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="email_status"
    )
    is_verified = models.BooleanField(default=False)
    verification_token = models.CharField(max_length=32, blank=True)

    @property
    def is_valid(self):
        """
        Check if the email status is valid.
        Used token is always invalid.
        Only the last token is be valid, if not verified.
        """
        if self.is_verified:
            return False
        last_email_status = (
            UserEmailStatus.objects.filter(user=self.user).order_by("-created").first()
        )
        if self.id == last_email_status.id:
            created = self.created
            now = timezone.now()
            if (now - created).days < EMAIL_TOKEN_VALIDITY:
                return True
        return False

    def __str__(self):
        return f"{self.user.username} email status"

    class Meta:
        verbose_name_plural = "User email statuses"
