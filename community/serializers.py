from rest_framework import serializers
from .models import UserModel, PostModel, PostCommentModel, LikeModel

class UserModel_serializer(serializers.ModelSerializer):
    # comments = Comment_model_serializer(many=True)
    class Meta:
        model = UserModel
        fields = '__all__'

class PostCommentModel_serializer(serializers.ModelSerializer):
    class Meta:
        model = PostCommentModel
        fields = '__all__'

class PostModel_serializer(serializers.ModelSerializer):
    # comment = MainCommentModel_serializer(many=True, allow_null=True, read_only=True)
    list = serializers.CharField(allow_blank=True)
    class Meta:
        model = PostModel
        fields = '__all__'

class LikeModel_serializer(serializers.ModelSerializer):
    class Meta:
        model = LikeModel
        fields = '__all__'
