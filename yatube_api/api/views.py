from rest_framework import viewsets, permissions
from api.serializers import (
    CommentSerializer, PostSerializer, GroupSerializer
)

from posts.models import Comment, Group, Post

UNSAFE_METHODS = ['PUT', 'PATCH', 'DELETE']


class OwnProfilePermission(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method not in UNSAFE_METHODS:
            return True
        return obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated, OwnProfilePermission)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticated, OwnProfilePermission)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user,
                        post=Post.objects.get(id=self.kwargs['post_id']))

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['post_id'])


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
