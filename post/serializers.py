from rest_framework import serializers

from post.models import Category, Post, Comment


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'title',)


class PostSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    comments = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    category = CategorySerializer(many=False, read_only=True)

    class Meta:
        model = Post
        fields = ('id','title', 'description', 'owner', 'comments',
                  'category', 'preview', 'quantity', 'address', 'phone',)


    def validate(self, attrs):
        print(attrs)
        return super().validate(attrs)


class CommentSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Comment
        fields = ('id', 'body', 'owner', 'post')