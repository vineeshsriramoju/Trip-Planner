# Generated by Django 2.1.7 on 2019-05-01 19:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('credits', '0015_auto_20190501_0722'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pending_redeem',
            name='transaction_id',
            field=models.CharField(default='37E0363E545D', max_length=14),
        ),
        migrations.AlterField(
            model_name='pending_transactions',
            name='transaction_id',
            field=models.CharField(default='ADD812F7AC34', max_length=14),
        ),
    ]
