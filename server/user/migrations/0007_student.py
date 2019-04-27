# Generated by Django 2.2 on 2019-04-24 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_user_user_fillln'),
    ]

    operations = [
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_number', models.IntegerField()),
                ('student_name', models.CharField(max_length=20)),
                ('student_university', models.CharField(max_length=50)),
                ('student_academy', models.CharField(max_length=50)),
                ('student_grade', models.IntegerField()),
                ('student_sex', models.SmallIntegerField(default=0)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
        ),
    ]
