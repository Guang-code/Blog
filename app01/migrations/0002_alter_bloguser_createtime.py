# Generated by Django 4.2.4 on 2023-11-15 08:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='createTime',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]