# from rest_framework import serializers
#
# from core.models import Team, Task, Notification, Comment, Message
# from users.api.serializers import UserSerializer
#
#
# class TaskSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Task
#         fields = "__all__"
#
#
# class TeamSerializer(serializers.ModelSerializer):
#     owner = UserSerializer(read_only=True)
#     class Meta:
#         model = Team
#         fields = "__all__"
#
#
# class NotificationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Notification
#         fields = "__all__"
#
#
# class CommentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Comment
#         fields = "__all__"
#         read_only_fields = ['user', 'task']
#
#
# class TaskDetailSerializer(serializers.ModelSerializer):
#     comments = CommentSerializer(many=True, read_only=True)
#     assigned_users = UserSerializer(many=True, read_only=True)
#     created_by = UserSerializer(read_only=True)
#     class Meta:
#         model = Task
#         fields = "__all__"
#
#
# class MessageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Message
#         fields = "__all__"
#
#
# class TeamDetailSerializer(serializers.ModelSerializer):
#     messages = MessageSerializer(many=True, read_only=True)
#     class Meta:
#         model = Team
#         fields = "__all__"

# chatgpt

from rest_framework import serializers
from core.models import Team, Task, Notification, Comment, Message
from users.api.serializers import UserSerializer


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"


class TeamSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)

    class Meta:
        model = Team
        fields = "__all__"


class TaskDetailSerializer(serializers.ModelSerializer):
    comments = serializers.SerializerMethodField()
    assigned_users = UserSerializer(many=True, read_only=True)
    created_by = UserSerializer(read_only=True)
    team = TeamSerializer(read_only=True)

    class Meta:
        model = Task
        fields = "__all__"

    def get_comments(self, obj):
        comments = obj.comments.all()
        return CommentSerializer(comments, many=True).data


class TeamDetailSerializer(serializers.ModelSerializer):
    messages = serializers.SerializerMethodField()
    owner = UserSerializer(read_only=True)
    admins = UserSerializer(many=True, read_only=True)
    members = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Team
        fields = "__all__"

    def get_messages(self, obj):
        messages = obj.messages.all()
        return MessageSerializer(messages, many=True).data


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = "__all__"


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = "__all__"
        read_only_fields = ["user", "task"]


class MessageSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Message
        fields = "__all__"
