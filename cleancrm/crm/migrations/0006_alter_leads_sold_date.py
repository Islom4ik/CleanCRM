# Generated by Django 4.2.14 on 2024-08-07 09:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0005_alter_leads_sold_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='leads',
            name='sold_date',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.MinLengthValidator(10)], verbose_name='Sold date'),
        ),
    ]
