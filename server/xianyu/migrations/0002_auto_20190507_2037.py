# Generated by Django 2.2 on 2019-05-07 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('xianyu', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Follower',
            new_name='Fan',
        ),
        migrations.RenameField(
            model_name='fan',
            old_name='follower_id',
            new_name='fan_id',
        ),
    ]