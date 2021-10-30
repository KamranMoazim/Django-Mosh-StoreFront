# Generated by Django 3.2.8 on 2021-10-19 12:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20211019_1205'),
    ]

    operations = [
        migrations.AddField(
            model_name='collection',
            name='featured_product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='store.product'),
        ),
        migrations.AddField(
            model_name='product',
            name='slug',
            field=models.SlugField(null=True),
        ),
        migrations.AlterField(
            model_name='customer',
            name='member_ship',
            field=models.CharField(choices=[('B', 'Bronze'), ('G', 'Gold'), ('S', 'Silver')], default='B', max_length=1),
        ),
        migrations.AlterField(
            model_name='order',
            name='member_ship',
            field=models.CharField(choices=[('F', 'Fail'), ('P', 'Pending'), ('C', 'Complete')], default='P', max_length=1),
        ),
    ]