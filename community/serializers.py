from rest_framework import serializers
from .models import UserModel, PostModel, PostCommentModel, PostModelView, PostModelViewWithPage

class UserModel_serializer(serializers.ModelSerializer):
    # comments = Comment_model_serializer(many=True)
    class Meta:
        model = UserModel
        fields = '__all__'

class PostModelView_serializer(serializers.ModelSerializer):
    class Meta:
        model = PostModelView
        fields = '__all__'


class PostCommentModel_serializer(serializers.ModelSerializer):
    class Meta:
        model = PostCommentModel
        fields = '__all__'

class PostModel_serializer(serializers.ModelSerializer):
    # comment = MainCommentModel_serializer(many=True, allow_null=True, read_only=True)
    class Meta:
        model = PostModel
        fields = '__all__'

class PostModelViewWithPage_serializer(serializers.ModelSerializer):
    class Meta:
        model = PostModelViewWithPage
        fields = '__all__'