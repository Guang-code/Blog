# Generated by Django 4.2.4 on 2023-11-16 05:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0016_alter_bloguser_createtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='gender',
            field=models.IntegerField(choices=[(0, '女'), (1, '男'), (2, '未知')], default=0, verbose_name='性别'),
        ),
    ]
