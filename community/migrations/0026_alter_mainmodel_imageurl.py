# Generated by Django 4.1.3 on 2022-11-30 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0025_delete_mainmodeldetail_mainmodel_comment_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainmodel',
            name='imageurl',
            field=models.TextField(default='', null=True),
        ),
    ]
