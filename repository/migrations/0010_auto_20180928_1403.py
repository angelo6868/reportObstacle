# Generated by Django 2.0.6 on 2018-09-28 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0009_auto_20180928_1228'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogtable',
            name='blog_title',
            field=models.CharField(default=None, max_length=128),
        ),
        migrations.AddField(
            model_name='usertable',
            name='user_nickname',
            field=models.CharField(default=None, max_length=32),
        ),
    ]