# Generated by Django 4.2.4 on 2023-11-15 12:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0008_alter_bloguser_createtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='createTime',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 15, 20, 15, 10, 748339)),
        ),
    ]
