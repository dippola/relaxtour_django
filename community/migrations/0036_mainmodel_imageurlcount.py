# Generated by Django 4.1.3 on 2022-12-05 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0035_mainmodel_commentcount'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainmodel',
            name='imageurlcount',
            field=models.IntegerField(default=0),
        ),
    ]