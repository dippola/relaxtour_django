# Generated by Django 4.1.3 on 2022-11-21 01:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0006_alter_mainmodel_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='token',
            field=models.TextField(blank=True, default='', null=True),
        ),
        migrations.AlterField(
            model_name='maincommentmodel',
            name='to',
            field=models.TextField(blank=True, default='', null=True),
        ),
    ]