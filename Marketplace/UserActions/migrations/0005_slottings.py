# Generated by Django 2.1 on 2020-05-30 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserActions', '0004_auto_20200530_1552'),
    ]

    operations = [
        migrations.CreateModel(
            name='Slottings',
            fields=[
                ('slot_id', models.AutoField(primary_key=True, serialize=False)),
                ('start_time', models.DateTimeField()),
                ('usage_count', models.IntegerField()),
            ],
        ),
    ]
