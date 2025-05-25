from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from . import views

router = DefaultRouter()
router.register('tasks', views.TaskViewSet)
task_router = NestedDefaultRouter(router, 'tasks', lookup='task')
task_router.register('comments', views.TaskCommentViewSet)
router.register('teams', views.TeamViewSet)
router.register('notifications', views.NotificationViewSet)

urlpatterns = router.urls + task_router.urls
