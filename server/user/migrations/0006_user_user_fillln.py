# Generated by Django 2.2 on 2019-04-24 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0005_remove_user_user_nearlogin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_fillln',
            field=models.SmallIntegerField(default=0),
        ),
    ]
