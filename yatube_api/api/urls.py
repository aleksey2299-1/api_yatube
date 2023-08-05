from rest_framework.authtoken import views
from rest_framework.routers import SimpleRouter
from django.urls import path, include

from api.views import (PostViewSet,
                       CommentViewSet,
                       GroupViewSet)

router = SimpleRouter()
router.register('posts', PostViewSet)
router.register(r'posts/(?P<post_id>\d+)/comments',
                CommentViewSet,
                basename='comments')
router.register('groups', GroupViewSet)

urlpatterns = [
    path('api-token-auth/', views.obtain_auth_token),
    path('', include(router.urls)),
]
