from rest_framework import serializers
from .models import UserModel, MainModel, QnaModel, MainCommentModel, QnaCommentModel, MainModelView, MainCommentModelView

class UserModel_serializer(serializers.ModelSerializer):
    # comments = Comment_model_serializer(many=True)
    class Meta:
        model = UserModel
        fields = '__all__'

class MainModelView_serializer(serializers.ModelSerializer):
    class Meta:
        model = MainModelView
        fields = '__all__'


class MainCommentModel_serializer(serializers.ModelSerializer):
    class Meta:
        model = MainCommentModel
        fields = '__all__'

class MainCommentModelView_serializer(serializers.ModelSerializer):
    class Meta:
        model = MainCommentModelView
        fields = '__all__'

class MainModel_serializer(serializers.ModelSerializer):
    comment = MainCommentModelView_serializer(many=True, allow_null=True, read_only=True)
    class Meta:
        model = MainModel
        fields = '__all__'

class QnaModel_serializer(serializers.ModelSerializer):
    # comments = Comment_model_serializer(many=True)
    class Meta:
        model = QnaModel
        fields = '__all__'



class QnaCommentModel_serializer(serializers.ModelSerializer):
    # comments = Comment_model_serializer(many=True)
    class Meta:
        model = QnaCommentModel
        fields = '__all__'