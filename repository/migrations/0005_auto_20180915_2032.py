# Generated by Django 2.0.6 on 2018-09-15 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0004_auto_20180915_1049'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='创建时间'),
        ),
        migrations.AlterField(
            model_name='usertable',
            name='user_fans',
            field=models.ManyToManyField(blank=True, related_name='user_flower', to='repository.UserTable'),
        ),
    ]
