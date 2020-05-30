# Generated by Django 2.1 on 2020-05-30 04:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='ClaimedItems',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('order_placed_date', models.DateTimeField(auto_now=True)),
                ('deadline_date', models.DateTimeField()),
                ('starting_bid', models.FloatField()),
                ('highest_bid', models.FloatField()),
                ('contact', models.IntegerField()),
                ('item_name', models.CharField(max_length=100)),
                ('item_description', models.CharField(blank=True, max_length=250)),
                ('image_url', models.FileField(upload_to='documents')),
                ('claimed_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='user_highest_bid_item_claimed', to=settings.AUTH_USER_MODEL)),
                ('upload_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('item_id', models.AutoField(primary_key=True, serialize=False)),
                ('item_price', models.FloatField()),
                ('item_name', models.CharField(max_length=100)),
                ('item_description', models.CharField(blank=True, max_length=250)),
                ('image_url', models.FileField(upload_to='documents')),
            ],
        ),
        migrations.CreateModel(
            name='Pincodes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pincode', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='pincode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserActions.Pincodes'),
        ),
        migrations.AddField(
            model_name='cart',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='UserActions.Item'),
        ),
    ]