# Generated by Django 4.2.10 on 2024-03-12 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0004_alter_tradingdays_day'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='price_age',
            field=models.IntegerField(choices=[(0, 'Adult'), (1, 'Student'), (2, 'Child')], default=0),
        ),
    ]