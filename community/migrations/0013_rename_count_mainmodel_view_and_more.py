# Generated by Django 4.1.3 on 2022-11-27 10:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0012_mainmodelview'),
    ]

    operations = [
        migrations.RenameField(
            model_name='mainmodel',
            old_name='count',
            new_name='view',
        ),
        migrations.RenameField(
            model_name='mainmodelview',
            old_name='count',
            new_name='commentcount',
        ),
    ]
