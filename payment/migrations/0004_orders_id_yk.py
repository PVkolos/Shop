# Generated by Django 5.1.2 on 2024-11-01 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_alter_orders_summ'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='id_yk',
            field=models.CharField(default='', max_length=100, verbose_name='ID из Yookassa'),
        ),
    ]
