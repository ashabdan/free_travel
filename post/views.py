from django_filters import rest_framework as filters
from rest_framework import generics, permissions, viewsets, status
from rest_framework.pagination import PageNumberPagination
from post import serializers
from post.models import Post, Comment, Category, Like
from post.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q


class PostPagination(PageNumberPagination):
    page_size = 10

class CommentPagination(PageNumberPagination):
    page_size = 20


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer
    pagination_class = PostPagination
    filter_backends = [filters.DjangoFilterBackend, ]
    filterset_fields = ('category', 'owner', )
    def get_permissions(self):
        if self.action == 'create':
            self.permission_classes = (permissions.IsAuthenticated, )
        elif self.action in ['update', 'partial-update', 'delete']:
            self.permission_classes = (IsOwnerOrReadOnly, )
        else:
            self.permission_classes = (permissions.AllowAny, )
        return super().get_permissions()

    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        product = self.get_object()
        obj, created = Like.objects.get_or_create(user=request.user.profile_customer, product=product)
        if not created:
            obj.like = not obj.like
            obj.save()
        liked_or_unliked = 'liked' if obj.like else 'unliked'
        return Response('Successfully {} product'.format(liked_or_unliked), status=status.HTTP_200_OK)

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.query_params.get('search', '')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) | Q(id__icontains=search) | Q(address__icontains=search))
        return queryset


class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    pagination_class = CommentPagination
    permission_classes = (IsOwnerOrReadOnly, permissions.IsAuthenticatedOrReadOnly)


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer
