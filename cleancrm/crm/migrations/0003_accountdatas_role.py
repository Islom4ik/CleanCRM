# Generated by Django 4.2.14 on 2024-08-07 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crm', '0002_alter_accountdatas_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountdatas',
            name='role',
            field=models.CharField(choices=[('Owner', 'Owner'), ('Operator', 'Operator')], default='Operator', max_length=8, verbose_name='Role'),
        ),
    ]
