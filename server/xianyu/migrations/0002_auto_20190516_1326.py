# Generated by Django 2.2 on 2019-05-16 13:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('xianyu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionnaire',
            name='questionnaire_deadline',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
