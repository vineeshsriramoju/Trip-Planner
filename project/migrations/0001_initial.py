# Generated by Django 2.1.3 on 2019-04-06 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='package',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('package_title', models.CharField(max_length=50, null='True')),
                ('train', models.CharField(max_length=60, null='True')),
                ('hotel', models.CharField(max_length=60, null='True')),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
