# Generated by Django 2.0.6 on 2018-09-22 05:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0007_auto_20180922_1232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commenttable',
            name='parent_comment_id',
        ),
        migrations.AddField(
            model_name='commenttable',
            name='create_time',
            field=models.DateTimeField(auto_now_add=True, default=None),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='commenttable',
            name='parent_comment',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.CommentTable'),
        ),
    ]
