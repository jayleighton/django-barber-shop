# Generated by Django 4.2.10 on 2024-03-07 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setup', '0003_service_created_on_service_updated_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tradingdays',
            name='day',
            field=models.IntegerField(choices=[(1, 'Monday - Friday'), (2, 'Saturday'), (3, 'Sunday')], unique=True),
        ),
    ]
