# Generated by Django 4.1.3 on 2022-11-28 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0017_alter_maincommentmodel_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mainmodeldetail',
            name='comment',
        ),
        migrations.AddField(
            model_name='mainmodeldetail',
            name='comment',
            field=models.ManyToManyField(to='community.maincommentmodel'),
        ),
    ]