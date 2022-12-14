# Generated by Django 4.1.3 on 2022-11-18 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('community', '0003_remove_maincommentmodel_email_remove_mainmodel_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usermodel',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='usermodel',
            name='provider',
            field=models.CharField(default='', max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='maincommentmodel',
            name='to',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mainmodel',
            name='imageurl',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mainmodel',
            name='list',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='qnacommentmodel',
            name='to',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='qnamodel',
            name='imageurl',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='imageurl',
            field=models.TextField(blank=True, null=True),
        ),
    ]
