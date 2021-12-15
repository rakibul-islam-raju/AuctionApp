# Generated by Django 4.0 on 2021-12-14 06:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_auctionproduct_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductBid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_bid', to='core.auctionproduct')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_bid', to='core.user')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
