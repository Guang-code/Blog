# Generated by Django 4.2.4 on 2023-11-16 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0017_alter_bloguser_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='gender',
            field=models.IntegerField(choices=[(0, '女'), (1, '男'), (2, '未知')], default=2, verbose_name='性别'),
        ),
    ]
