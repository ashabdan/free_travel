from rest_framework import serializers

from post.models import Category, Post, Comment, Like


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name',)


class PostSerializer(serializers.ModelSerializer):
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Post
        fields = ('id','title', 'description', 'owner', 'comments',
                  'category', 'preview', 'quantity', 'address', 'phone', )

    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)

    def to_representation(self, instance):
        representation = super(PostSerializer, self).to_representation(instance)
        action = self.context.get('action')
        likes = LikeSerializer(instance.likes.filter(like=True), many=True).data
        if action == 'list':
            representation['likes'] = len(likes)
        if action == 'retrieve':
            representation['likes'] = likes
        return representation


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = ('id', 'body', 'owner', 'post')


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('owner',)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['owner'] = instance.owner.email
        return representation