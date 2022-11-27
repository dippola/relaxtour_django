from django.db import models

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

class MainModelView(models.Model):
    parent_id = models.IntegerField(null=True)
    parent_user = models.IntegerField()
    nickname = models.TextField(null=True, default='')
    date = models.TextField()
    title = models.TextField()
    imageurl = models.TextField()
    commentcount = models.IntegerField()
    like = models.IntegerField()

class MainModel(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    parent_user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=30)
    body = models.TextField(null=False)
    imageurl = models.TextField(null=True, blank=True)
    view = models.PositiveIntegerField(default=0)
    like = models.PositiveIntegerField(default=0)
    list = models.TextField(null=True, default='')
    class Meta:
        ordering = ['-date']

class MainCommentModel(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    parent_id = models.ForeignKey(MainModel, on_delete=models.CASCADE)
    parent_user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    body = models.TextField(null=False)
    to = models.TextField(null=True, blank=True, default='')
    class Meta:
        ordering = ['-date']

class QnaModel(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    parent_user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    uid = models.CharField(max_length=50, null=True, default='')
    title = models.CharField(max_length=30)
    body = models.TextField(null=False)
    imageurl = models.TextField(null=True, blank=True)
    count = models.PositiveIntegerField(default=0)
    like = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ['-date']

class QnaCommentModel(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=True)
    parent_id = models.ForeignKey(QnaModel, on_delete=models.CASCADE)
    parent_user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    uid = models.CharField(max_length=50, null=True, default='')
    body = models.TextField(null=False)
    to = models.TextField(null=True, blank=True)
    class Meta:
        ordering = ['-date']
