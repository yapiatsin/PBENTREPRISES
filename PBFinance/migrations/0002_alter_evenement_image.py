# Generated by Django 5.0 on 2024-02-18 16:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PBFinance', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evenement',
            name='image',
            field=models.FileField(upload_to='evenement'),
        ),
    ]
