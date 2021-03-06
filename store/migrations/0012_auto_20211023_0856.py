# Generated by Django 3.2.8 on 2021-10-23 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0011_auto_20211023_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='member_ship',
            field=models.CharField(choices=[('G', 'Gold'), ('B', 'Bronze'), ('S', 'Silver')], default='B', max_length=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('P', 'Pending'), ('C', 'Complete'), ('F', 'Fail')], default='P', max_length=1),
        ),
    ]
