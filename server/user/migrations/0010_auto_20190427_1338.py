# Generated by Django 2.2 on 2019-04-27 05:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0009_order_pickorder_publishorder'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_complish',
            new_name='order_complished',
        ),
        migrations.RenameField(
            model_name='order',
            old_name='order_pick',
            new_name='order_picked',
        ),
        migrations.CreateModel(
            name='Followings',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('folloings_id', models.IntegerField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
        ),
        migrations.CreateModel(
            name='Fans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fans_id', models.IntegerField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
        ),
    ]
