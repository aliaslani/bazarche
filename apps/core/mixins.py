from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.models import AbstractUser
from django.shortcuts import redirect, resolve_url
from django.utils.cache import patch_vary_headers
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View
from .exceptions import ApplicationError


class StaffRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        return user.is_active and user.is_staff

class OwnerQueryMixin:
    owner_field = "user"
    def get_queryset(self):
        return super().get_queryset().filter(**{self.owner_field: self.request.user})


