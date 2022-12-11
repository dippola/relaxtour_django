from django.db import models
from django.contrib.postgres.fields import ArrayField

class UserModel(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    email = models.EmailField(null=True, default='')
    uid = models.CharField(max_length=50, null=True, default='')
    nickname = models.CharField(max_length=14, null=True, default='', blank=True)
    imageurl = models.TextField(null=True, default='', blank=True)
    provider = models.CharField(max_length=20, null=True, default='')
    token = models.TextField(null=True, default='', blank=True)
    notification = models.BooleanField(default=True)
    class Meta:
        ordering = ['-id']



class PostModelView(models.Model):#only GET
    CATEGORY = (
        ("FREE", "free"),
        ('QNA', 'qna')
    )
    parent_id = models.IntegerField(null=True)
    parent_user = models.IntegerField()
    nickname = models.TextField(null=True, default='')
    user_image = models.TextField(default='')
    category = models.CharField(max_length=20, choices=CATEGORY)
    date = models.TextField()
    title = models.TextField()
    imageurl = models.TextField()
    imageurlcount = models.IntegerField(default=0)
    commentcount = models.IntegerField()
    view = models.IntegerField(default=0)
    like = models.IntegerField(default=0)



class PostModel(models.Model):
    CATEGORY = (
        ("FREE", "free"),
        ('QNA', 'qna')
    )
    id = models.AutoField(primary_key=True, null=False, blank=False)
    parent_user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    nickname = models.TextField(null=True, default='')
    user_url = models.TextField(null=True, default='')
    category = models.CharField(max_length=20, choices=CATEGORY)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=60)
    body = models.TextField(null=False)
    imageurl = models.TextField(null=True, default='')
    view = models.PositiveIntegerField(default=0)
    like = models.PositiveIntegerField(default=0)
    list = models.TextField(null=True, default='')
    commentcount = models.IntegerField(default=0)
    class Meta:
        ordering = ['-date']

class PostCommentModel(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    parent_id = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    parent_user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    body = models.TextField(null=False)
    nickname = models.TextField(default='')
    user_url = models.TextField(default='')
    to_id = models.IntegerField(default=0)
    to_nickname = models.TextField(default='')
    class Meta:
        ordering = ['date']

class LikeModel(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    parent_id = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    user_ids = models.ForeignKey(UserModel, on_delete=models.PROTECT)