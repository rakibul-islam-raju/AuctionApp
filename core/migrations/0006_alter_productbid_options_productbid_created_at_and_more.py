# Generated by Django 4.0 on 2021-12-14 07:07

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_productbid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productbid',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='productbid',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='productbid',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]