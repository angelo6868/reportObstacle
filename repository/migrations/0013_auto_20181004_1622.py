# Generated by Django 2.0.6 on 2018-10-04 08:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('repository', '0012_auto_20181004_1608'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporttable',
            name='processor',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_processor', to='repository.UserTable', verbose_name='报障单处理用户'),
        ),
    ]