from django.contrib import admin

from .models import User, Position, Region, District


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "username", "position", "region", "date_joined")
    search_fields = ("id", "first_name", "last_name", "username", "position", "region")
    ordering = ("id", "username", "first_name", "last_name")


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "rank")
    search_fields = ("id", "name")
    ordering = ("id", "name", "rank")


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("id", "name")
    search_fields = ("id", "name")
    ordering = ("id", "name")


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ("id", "region", "name")
    search_fields = ("id", "name", "region")
    ordering = ("id", "name")
    list_filter = ("region",)
