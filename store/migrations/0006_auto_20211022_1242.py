# Generated by Django 3.2.8 on 2021-10-22 12:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0005_auto_20211022_1227'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='member_ship',
        ),
        migrations.AddField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('F', 'Fail'), ('C', 'Complete'), ('P', 'Pending')], default='P', max_length=1),
        ),
    ]
