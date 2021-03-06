# Generated by Django 2.0.6 on 2018-10-12 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0015_reporttable_solution_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blogtable',
            name='blog_title',
            field=models.CharField(default=None, max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='blogtable',
            name='summary',
            field=models.CharField(max_length=128, null=True, verbose_name='博客简介'),
        ),
        migrations.AlterField(
            model_name='blogtable',
            name='theme',
            field=models.CharField(max_length=32, null=True, verbose_name='博客主题'),
        ),
    ]
