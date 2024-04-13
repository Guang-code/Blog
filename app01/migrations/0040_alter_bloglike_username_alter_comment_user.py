# Generated by Django 4.2.7 on 2024-03-16 14:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0039_alter_comment_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bloglike',
            name='username',
            field=models.ForeignKey(db_column='username_username', on_delete=django.db.models.deletion.CASCADE, to='app01.bloguser'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.bloguser', verbose_name='评论用户'),
        ),
    ]
