# Generated by Django 4.1.3 on 2022-11-28 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0014_mainmodelview_parent_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainmodelview',
            name='nickname',
            field=models.TextField(default='', null=True),
        ),
        migrations.AddField(
            model_name='mainmodelview',
            name='view',
            field=models.IntegerField(default=0),
        ),
    ]
