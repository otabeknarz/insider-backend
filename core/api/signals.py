from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.conf import settings
from django.utils import timezone

from users.models import User
from core.models import Task, Team, Notification, Comment
import requests


def send_telegram_message(chat_id, text):
    telegram_bot_api_url = (
        f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    )
    requests.post(telegram_bot_api_url, data={"chat_id": chat_id, "text": text})


@receiver(post_save, sender=Task)
def notify_assigned_user_on_task_create(sender, instance, created, **kwargs):
    if created and instance.assigned_user_id:
        deadline_str = ""
        if instance.deadline:
            deadline_local = timezone.localtime(instance.deadline)
            deadline_str = f"\n📅 Deadline: {deadline_local.strftime('%Y-%m-%d %H:%M')}"

        message = (
            f"@{instance.created_by.username} has assigned you a task:"
            f"\n{settings.TASK_URL_WITH_ID(instance.id)}"
            f"{deadline_str}"
        )
        Notification.objects.create(
            task=instance,
            team=instance.team,
            user=instance.assigned_user,
            message=message
        )


@receiver(m2m_changed, sender=Team.members.through)
def notify_on_team_join(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        for user_id in pk_set:
            user = User.objects.get(pk=user_id)
            message = f"You have been added to the \"{instance.name}\" team.\n{settings.TEAM_URL_WITH_ID(instance.id)}"
            Notification.objects.create(
                team=instance,
                user=user,
                message=message
            )


@receiver(post_save, sender=Comment)
def notify_comment(sender, instance, created, **kwargs):
    if created and instance.task:
        message = f"@{instance.user} commented on task {settings.TASK_URL_WITH_ID(instance.task.id)}\n{instance.message}"
        for user in instance.task.assigned_users.all():
            Notification.objects.create(task=instance.task, user=user, message=message)
        message = f"@{instance.user} commented on your task {settings.TASK_URL_WITH_ID(instance.task.id)}\n{instance.message}"
        Notification.objects.create(
            task=instance.task, user_id=instance.task.created_by.id, message=message
        )


@receiver(post_save, sender=Notification)
def send_notification_telegram(sender, instance, created, **kwargs):
    if created and instance.user:
        send_telegram_message(instance.user.id, instance.message)
