# Generated by Django 4.2 on 2024-09-02 02:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_accounts_supervisor'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='doc_controller',
            field=models.BooleanField(default=False),
        ),
    ]
