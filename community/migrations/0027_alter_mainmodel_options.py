# Generated by Django 4.1.3 on 2022-12-01 12:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0026_alter_mainmodel_imageurl'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mainmodel',
            options={'ordering': ['-date']},
        ),
    ]
