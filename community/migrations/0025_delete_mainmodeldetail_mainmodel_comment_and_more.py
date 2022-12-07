# Generated by Django 4.1.3 on 2022-11-29 11:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0024_mainmodeldetail_remove_mainmodel_comment_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MainModelDetail',
        ),
        migrations.AddField(
            model_name='mainmodel',
            name='comment',
            field=models.ManyToManyField(to='community.maincommentmodel'),
        ),
        migrations.AddField(
            model_name='mainmodel',
            name='nickname',
            field=models.TextField(default='', null=True),
        ),
        migrations.AddField(
            model_name='mainmodel',
            name='user_url',
            field=models.TextField(default='', null=True),
        ),
    ]
