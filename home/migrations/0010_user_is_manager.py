# Generated by Django 4.2.10 on 2024-03-06 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_delete_info_delete_tradingdays'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_manager',
            field=models.BooleanField(default=False),
        ),
    ]
