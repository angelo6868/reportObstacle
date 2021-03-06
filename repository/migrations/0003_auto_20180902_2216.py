# Generated by Django 2.0.6 on 2018-09-02 14:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0002_auto_20180902_2050'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='repository.BlogTable', verbose_name='文章所在博客'),
        ),
        migrations.AlterField(
            model_name='classification',
            name='caption',
            field=models.CharField(max_length=32),
        ),
        migrations.AlterField(
            model_name='label',
            name='caption',
            field=models.CharField(max_length=32),
        ),
    ]
