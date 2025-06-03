# from rest_framework import viewsets
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework import filters
# from django_filters.rest_framework import DjangoFilterBackend
#
# from core.models import Task, Team, Notification, Comment
# from .serializers import (
#     TaskSerializer,
#     TeamSerializer,
#     NotificationSerializer,
#     CommentSerializer,
#     TaskDetailSerializer,
#     TeamDetailSerializer
# )
#
#
# class TaskViewSet(viewsets.ModelViewSet):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer
#     pagination_class = LimitOffsetPagination
#
#     filter_backends = [
#         DjangoFilterBackend,
#         filters.SearchFilter,
#         filters.OrderingFilter,
#     ]
#
#     filterset_fields = ['assigned_users', 'team']
#     search_fields = ['name', 'description']
#     ordering_fields = ['created_at']
#     ordering = ['-created_at']
#
#     def get_serializer_class(self):
#         if self.action == 'retrieve' and "comments" in self.request.path:
#             return CommentSerializer
#         if self.action == 'retrieve':
#             return TaskDetailSerializer
#         return TaskSerializer
#
#     def get_queryset(self):
#         if self.action == 'retrieve' and 'comments' in self.request.path:
#             task_id = self.kwargs.get('id')
#             return Comment.objects.filter(task_id=task_id)
#
#         return Task.objects.all()
#
#     def perform_create(self, serializer):
#         serializer.save(created_by=self.request.user)
#
#
# class TeamViewSet(viewsets.ModelViewSet):
#     queryset = Team.objects.all()
#     serializer_class = TeamSerializer
#     pagination_class = LimitOffsetPagination
#     filter_backends = [
#         DjangoFilterBackend,
#         filters.SearchFilter,
#         filters.OrderingFilter,
#     ]
#
#     filterset_fields = ['members']
#     search_fields = ['name', 'description']
#     ordering_fields = ['created_at']
#
#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return TeamDetailSerializer
#         return TeamSerializer
#
#     def perform_create(self, serializer):
#         serializer.save(owner=self.request.user)
#
#
# class NotificationViewSet(viewsets.ModelViewSet):
#     queryset = Notification.objects.all()
#     serializer_class = NotificationSerializer
#     pagination_class = LimitOffsetPagination
#
#     def get_queryset(self):
#         queryset = Notification.objects.filter(user=self.request.user)
#         return queryset
#
#
# class TaskCommentViewSet(viewsets.ModelViewSet):
#     queryset = Comment.objects.all()
#     serializer_class = CommentSerializer
#     pagination_class = LimitOffsetPagination
#
#     def get_queryset(self):
#         queryset = Comment.objects.filter(task=self.kwargs.get('task_pk'))
#         return queryset
#
#     def perform_create(self, serializer):
#         task_pk = self.kwargs.get('task_pk')
#         serializer.save(user=self.request.user, task_id=task_pk)


from rest_framework import viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q

from core.models import Task, Team, Notification, Comment
from .serializers import (
    TaskSerializer,
    TaskDetailSerializer,
    TeamSerializer,
    TeamDetailSerializer,
    NotificationSerializer,
    CommentSerializer
)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().select_related('created_by', 'team').prefetch_related('assigned_users', 'comments')
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['assigned_users', 'team']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TaskDetailSerializer
        return TaskSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(
            Q(created_by=user) | Q(assigned_users=user)
        ).distinct()

    @action(detail=False, methods=['get'], url_path='by-me')
    def by_me(self, request):
        tasks = Task.objects.filter(created_by=request.user)
        page = self.paginate_queryset(tasks)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)

    @action(detail=False, methods=['get'], url_path='to-me')
    def to_me(self, request):
        tasks = Task.objects.filter(assigned_users=request.user)
        page = self.paginate_queryset(tasks)
        serializer = self.get_serializer(page, many=True)
        return self.get_paginated_response(serializer.data)


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().select_related('owner').prefetch_related('admins', 'members', 'messages')
    pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['members']
    search_fields = ['name', 'description']
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TeamDetailSerializer
        return TeamSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        data = self.request.data
        being_removed_members = data.get('members_remove', [])
        being_removed_admins = data.get('admins_remove', [])

        if being_removed_members:
            # Assuming they are IDs:
            members_to_remove = serializer.instance.members.filter(id__in=being_removed_members)
            serializer.instance.members.remove(*members_to_remove)

        if being_removed_admins:
            admins_to_remove = serializer.instance.admins.filter(id__in=being_removed_admins)
            serializer.instance.admins.remove(*admins_to_remove)

        serializer.save()


class TeamTaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Task.objects.filter(team_id=self.kwargs['team_pk'])

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user, team_id=self.kwargs['team_pk'])


class NotificationViewSet(viewsets.ModelViewSet):
    serializer_class = NotificationSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user)

class TaskCommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = LimitOffsetPagination

    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs['task_pk'])

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, task_id=self.kwargs['task_pk'])
