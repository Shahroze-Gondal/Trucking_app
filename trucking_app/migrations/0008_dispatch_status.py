# Generated by Django 4.1.1 on 2022-10-10 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trucking_app', '0007_remove_dispatch_owner'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispatch',
            name='status',
            field=models.CharField(choices=[('Scheduled', 'Scheduled'), ('In Transit', 'In Transit'), ('Delivered', 'Delivered')], max_length=20, null=True),
        ),
    ]