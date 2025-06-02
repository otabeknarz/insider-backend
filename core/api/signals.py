# from django.db.models.signals import post_save, m2m_changed
# from django.dispatch import receiver
# from django.conf import settings
#
# from core.models import Task, Team, Notification, Comment
#
#
# @receiver(m2m_changed, sender=Task.assigned_users.through)
# def create_notifications_on_assignment(sender, instance, action, pk_set, **kwargs):
#     message = f"@{instance.created_by} have assigned task to you.\n{settings.TASK_URL_WITH_ID(instance.id)}"
#     if action == "post_add":
#         for user_id in pk_set:
#             Notification.objects.create(
#                 task=instance,
#                 user_id=user_id,
#                 message=message
#             )
#
#
# @receiver(m2m_changed, sender=Team.members.through)
# def create_notifications_on_team_adding(sender, instance, action, pk_set, **kwargs):
#     message = f"You have been added to the {sender.team.name} team.\n{settings.TEAM_URL_WITH_ID(instance.id)}"
#     if action == "post_add":
#         for user_id in pk_set:
#             Notification.objects.create(
#                 task=instance,
#                 user_id=user_id,
#                 message=message
#             )
#
#
# @receiver(post_save, sender=Comment)
# def create_comment_notification(sender, instance, created, **kwargs):
#     message = f"@{instance.user} commented in task {settings.TASK_URL_WITH_ID(instance.task.id)} \n{instance.message}"
#     if created and instance.task:
#         for user in instance.task.assigned_users.all():
#             Notification.objects.create(
#                 task=instance.task,
#                 user=user,
#                 message=message
#             )

# chatgpt's code

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver
from django.conf import settings

from core.models import Task, Team, Notification, Comment
from users.models import User
import requests

def send_telegram_message(chat_id, text):
    telegram_bot_api_url = (
        f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
    )
    requests.post(telegram_bot_api_url, data={'chat_id': chat_id, 'text': text})

@receiver(m2m_changed, sender=Task.assigned_users.through)
def notify_assigned_users(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        message = f"@{instance.created_by} has assigned you a task.\n{settings.TASK_URL_WITH_ID(instance.id)}"
        for user_id in pk_set:
            Notification.objects.create(
                task=instance,
                user_id=user_id,
                message=message
            )


@receiver(m2m_changed, sender=Team.members.through)
def notify_team_members(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        message = f"You have been added to the {instance.name} team.\n{settings.TEAM_URL_WITH_ID(instance.id)}"
        for user_id in pk_set:
            Notification.objects.create(
                team=instance,
                user_id=user_id,
                message=message
            )


@receiver(post_save, sender=Comment)
def notify_comment(sender, instance, created, **kwargs):
    if created and instance.task:
        message = f"@{instance.user} commented on task {settings.TASK_URL_WITH_ID(instance.task.id)}\n{instance.message}"
        for user in instance.task.assigned_users.all():
            Notification.objects.create(
                task=instance.task,
                user=user,
                message=message
            )
        message = f"@{instance.user} commented on your task {settings.TASK_URL_WITH_ID(instance.task.id)}\n{instance.message}"
        Notification.objects.create(
            task=instance,
            user_id=instance.created_by.id,
            message=message
        )


@receiver(post_save, sender=Notification)
def send_notification_telegram(sender, instance, created, **kwargs):
    if created and instance.user:
        send_telegram_message(instance.user.id, instance.message)
