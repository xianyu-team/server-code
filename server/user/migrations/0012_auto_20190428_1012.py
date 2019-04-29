# Generated by Django 2.2 on 2019-04-28 02:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0011_auto_20190427_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pickorder',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order'),
        ),
        migrations.AlterField(
            model_name='publishorder',
            name='order_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.Order'),
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
