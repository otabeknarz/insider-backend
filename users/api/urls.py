from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.urls import path

from users.api.views import UserViewSet, RegionViewSet, DistrictViewSet, PositionViewSet

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('regions', RegionViewSet)
router.register('districts', DistrictViewSet)
router.register('positions', PositionViewSet)

auth_urls = [
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
]

urlpatterns = auth_urls + router.urls
