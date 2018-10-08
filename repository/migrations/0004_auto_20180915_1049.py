# Generated by Django 2.0.6 on 2018-09-15 02:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0003_auto_20180902_2216'),
    ]

    operations = [
        migrations.AddField(
            model_name='classification',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.UserTable'),
        ),
        migrations.AddField(
            model_name='label',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='repository.UserTable'),
        ),
    ]
