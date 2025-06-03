# from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
#
# from . import views
#
# router = DefaultRouter()
# router.register('tasks', views.TaskViewSet)
# task_router = NestedDefaultRouter(router, 'tasks', lookup='task')
# task_router.register('comments', views.TaskCommentViewSet)
# router.register('teams', views.TeamViewSet)
# router.register('notifications', views.NotificationViewSet)
#
# urlpatterns = router.urls + task_router.urls


from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter
from . import views

router = DefaultRouter()
router.register(r'tasks', views.TaskViewSet, basename='task')
router.register(r'teams', views.TeamViewSet, basename='team')
router.register(r'notifications', views.NotificationViewSet, basename='notification')

team_router = NestedDefaultRouter(router, r'teams', lookup='team')
team_router.register(r'tasks', views.TeamTaskViewSet, basename='team-tasks')

task_router = NestedDefaultRouter(router, r'tasks', lookup='task')
task_router.register(r'comments', views.TaskCommentViewSet, basename='task-comments')

urlpatterns = router.urls + task_router.urls + team_router.urls
