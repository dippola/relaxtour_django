# Generated by Django 4.1.3 on 2022-12-02 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0027_alter_mainmodel_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='maincommentmodel',
            name='nickname',
            field=models.TextField(default=''),
        ),
        migrations.AddField(
            model_name='maincommentmodel',
            name='user_url',
            field=models.TextField(default=''),
        ),
    ]
