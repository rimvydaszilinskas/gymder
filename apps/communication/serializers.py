from rest_framework import serializers

from apps.users.serializers import UserSerializer

from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)
    user = UserSerializer(read_only=True)
    body = serializers.CharField(max_length=500)
    date = serializers.DateTimeField(source='created_at', read_only=True)
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = (
            'uuid',
            'body',
            'date',
            'user',
            'created_at',
            'comments'
        )

    def get_comments(self, obj):
        return len(obj.comments.filter(is_deleted=False))

    def update(self, instance, validated_data):
        instance.body = validated_data['body']
        instance.save(update_fields=['body'])

        return instance

    def save(self, **kwargs):
        if self.instance is None:
            if 'user' not in kwargs:
                raise Exception('user is not defined')

            # create action
            self.instance = Post.objects.create(
                body=self.validated_data['body'],
                user=kwargs['user'],
                group=kwargs.get('group', None),
                activity=kwargs.get('activity', None))
        else:
            self.instance = self.update(self.instance, self.validated_data)

        return self.instance


class CommentSerializer(serializers.ModelSerializer):
    uuid = serializers.UUIDField(format='hex', read_only=True)
    user = UserSerializer(read_only=True)
    post = serializers.UUIDField(format='hex', read_only=True, source='post.uuid')
    body = serializers.CharField(max_length=500)
    date = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Comment
        fields = (
            'uuid',
            'user',
            'post',
            'body',
            'date'
        )

    def update(self, instance, validated_data):
        instance.body = validated_data['body']
        instance.save(update_fields=['body'])

        return instance

    def save(self, **kwargs):
        if self.instance is None:
            if 'user' not in kwargs or 'post' not in kwargs:
                raise Exception('user/post not defined')
            
            self.instance = Comment.objects.create(
                body=self.validated_data['body'],
                user=kwargs['user'],
                post=kwargs['post'])
        else:
            self.instance = self.update(self.instance, self.validated_data)

        return self.instance


class FullPostSerializer(PostSerializer):
    """
    Read only serializer for packaging the whole full post with comments
    """
    comments = serializers.SerializerMethodField()

    def get_comments(self, obj):
        comments = obj.comments.filter(is_deleted=False)

        return CommentSerializer(comments, many=True).data
