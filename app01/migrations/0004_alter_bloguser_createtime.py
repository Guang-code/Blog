# Generated by Django 4.2.4 on 2023-11-15 08:57

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_alter_bloguser_createtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='createTime',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2023, 11, 15, 8, 57, 50, 321288, tzinfo=datetime.timezone.utc)),
            preserve_default=False,
        ),
    ]
