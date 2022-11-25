from rest_framework import serializers
from .models import UserModel, MainModel, QnaModel, MainCommentModel, QnaCommentModel

class UserModel_serializer(serializers.ModelSerializer):
    # comments = Comment_model_serializer(many=True)
    class Meta:
        model = UserModel
        fields = '__all__'

class UserModel_Notification_serializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ('notification')

class MainModel_serializer(serializers.ModelSerializer):
    class Meta:
        model = MainModel
        fields = '__all__'
        # fields = ('uid', 'nickname', 'body')

class QnaModel_serializer(serializers.ModelSerializer):
    # comments = Comment_model_serializer(many=True)
    class Meta:
        model = QnaModel
        fields = '__all__'

class MainCommentModel_serializer(serializers.ModelSerializer):
    # comments = Comment_model_serializer(many=True)
    class Meta:
        model = MainCommentModel
        fields = '__all__'

class QnaCommentModel_serializer(serializers.ModelSerializer):
    # comments = Comment_model_serializer(many=True)
    class Meta:
        model = QnaCommentModel
        fields = '__all__'