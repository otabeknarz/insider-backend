from django.db import models
from django.contrib.auth.models import AbstractUser

import random
import string

from insider.base_model import BaseModel


def get_random_id(k=12) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=k))


class Position(BaseModel):
    id = models.CharField(primary_key=True, default=get_random_id, max_length=40)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    rank = models.IntegerField(default=100)

    def __str__(self):
        return self.name


class User(AbstractUser):
    id = models.CharField(primary_key=True, default=get_random_id, unique=True)
    position = models.ForeignKey(
        Position, on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )
    region = models.ForeignKey(
        "Region", on_delete=models.SET_NULL, null=True, blank=True, related_name="users"
    )
    district = models.ForeignKey(
        "District",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )

    email = models.EmailField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Region(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class District(BaseModel):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="districts",
    )

    def __str__(self):
        return self.name
