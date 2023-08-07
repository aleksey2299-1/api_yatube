from django.shortcuts import get_object_or_404

from posts.models import Comment, Group, Post
from rest_framework import permissions, viewsets

from api.serializers import CommentSerializer, GroupSerializer, PostSerializer
from api.permissions import OwnProfilePermission


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
                        post=get_object_or_404(Post,
                                               id=self.kwargs['post_id']))

    def get_queryset(self):
        return Comment.objects.filter(post=self.kwargs['post_id'])


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
