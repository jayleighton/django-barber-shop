# Generated by Django 4.2.10 on 2024-03-16 14:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_alter_user_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['id']},
        ),
    ]