from django.contrib import admin

from .models import User, UserEmailStatus

admin.site.register(User)
admin.site.register(UserEmailStatus)
