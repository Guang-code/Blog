# Generated by Django 4.2.7 on 2024-03-17 04:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0040_alter_bloglike_username_alter_comment_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bloglike',
            old_name='save',
            new_name='collect',
        ),
    ]