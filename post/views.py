from django_filters import rest_framework as filters
from rest_framework import generics, permissions

from post import serializers
from post.models import Post, Comment, Category
from post.permissions import IsOwnerOrReadOnly


class PostListView(generics.ListAPIView):
    """Endpoint for retrieve all posts
    """
    queryset = Post.objects.select_related('owner', 'category')
    serializer_class = serializers.PostSerializer
    filter_backends = (filters.DjangoFilterBackend, )
    filterset_fields = ('title', 'category', 'owner',)


class PostCreateView(generics.CreateAPIView):
    """Endpoint for create post: only authenticeted user
    """
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetailView(generics.RetrieveAPIView):
    """Endpoint for retrieve single post
    """
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer


class PostDeleteView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)


class PostUpdateView(generics.UpdateAPIView ):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
