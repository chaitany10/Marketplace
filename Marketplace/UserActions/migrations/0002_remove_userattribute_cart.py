# Generated by Django 2.1 on 2020-05-30 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('UserActions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userattribute',
            name='cart',
        ),
    ]
