from django.db import models
import requests
from django.conf import settings

from users.models import User, get_random_id
from insider.base_model import BaseModel


def send_telegram_message(chat_id, text):
    try:
        url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {"chat_id": chat_id, "text": text}
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Telegram error: {e}")


class Team(BaseModel):
    id = models.CharField(primary_key=True, default=get_random_id, max_length=40)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    owner = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="my_owned_teams"
    )
    admins = models.ManyToManyField(User, related_name="my_admin_teams", blank=True)
    members = models.ManyToManyField(User, related_name="teams", blank=True)

    def __str__(self):
        return f"Team - {self.name}"

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new and self.owner:
            self.admins.add(self.owner)
            self.members.add(self.owner)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "Teams"


class Task(BaseModel):
    class StatusChoices(models.IntegerChoices):
        ASSIGNED = 1, "ASSIGNED"
        RECEIVED = 2, "RECEIVED"
        IN_PROCESS = 3, "IN_PROCESS"
        COMPLETED = 4, "COMPLETED"

    class PriorityChoices(models.IntegerChoices):
        MEDIUM = 1, "DEFAULT"
        HIGH = 2, "HIGH"

    id = models.CharField(primary_key=True, default=get_random_id, max_length=40)
    name = models.CharField(max_length=1000)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="tasks"
    )
    assigned_user = models.ForeignKey(
        User, related_name="assigned_tasks", on_delete=models.SET_NULL, null=True
    )
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, related_name="tasks"
    )
    status = models.IntegerField(
        choices=StatusChoices.choices, default=StatusChoices.ASSIGNED
    )
    is_checked = models.BooleanField(default=False)
    priority = models.IntegerField(
        choices=PriorityChoices.choices, default=PriorityChoices.MEDIUM
    )
    deadline = models.DateTimeField(null=True, blank=True)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.created_by} - {self.name}"


class Notification(BaseModel):
    id = models.CharField(primary_key=True, default=get_random_id, max_length=40)
    task = models.ForeignKey(
        Task, on_delete=models.SET_NULL, null=True, related_name="notifications"
    )
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, related_name="notifications"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="notifications"
    )
    message = models.TextField(null=True, blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.task} - {self.user}"


class Message(BaseModel):
    team = models.ForeignKey(
        Team, on_delete=models.SET_NULL, null=True, related_name="messages"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="messages"
    )
    message = models.TextField(null=True, blank=True)
    reply_to = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="replied_messages",
    )
    read_users = models.ManyToManyField(User, related_name="read_messages", blank=True)

    def __str__(self):
        return f"Message {self.team} - {self.user}"


class Comment(BaseModel):
    task = models.ForeignKey(
        Task, on_delete=models.SET_NULL, null=True, related_name="comments"
    )
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="comments"
    )
    message = models.TextField(null=True, blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Comment {self.task} - {self.user}"
