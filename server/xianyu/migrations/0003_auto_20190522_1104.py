# Generated by Django 2.2 on 2019-05-22 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('xianyu', '0002_auto_20190516_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='student_number',
            field=models.CharField(max_length=20),
        ),
    ]