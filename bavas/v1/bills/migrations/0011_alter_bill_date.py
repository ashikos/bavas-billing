# Generated by Django 4.2.10 on 2024-08-17 05:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bills', '0010_alter_bill_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='date',
            field=models.DateField(blank=True, default=datetime.date.today, null=True),
        ),
    ]
