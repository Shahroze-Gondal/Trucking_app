# Generated by Django 4.1.1 on 2022-09-19 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trucking_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dispatch',
            name='pod',
            field=models.ImageField(blank=True, upload_to=''),
        ),
    ]