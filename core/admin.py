from django.contrib import admin
from .models import Team, Task, Notification, Comment, Message


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('created_at',)
    ordering = ('-created_at',)


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'created_by', 'priority', 'deadline', 'created_at')
    search_fields = ('name', 'description')
    list_filter = ('priority', 'created_at')
    ordering = ('-created_at',)
    raw_id_fields = ('team', 'created_by')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'is_read', 'created_at')
    search_fields = ('message',)
    list_filter = ('is_read', 'created_at')
    ordering = ('-created_at',)
    raw_id_fields = ('task', 'user', 'team')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'user', 'is_read', 'created_at')
    search_fields = ('message',)
    list_filter = ('is_read', 'created_at')
    ordering = ('-created_at',)
    raw_id_fields = ('task', 'user')


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('team', 'user', 'created_at')
    search_fields = ('message',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    raw_id_fields = ('team', 'user', 'reply_to')
