# Generated by Django 4.2.4 on 2023-11-15 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0004_alter_bloguser_createtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloguser',
            name='createTime',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
