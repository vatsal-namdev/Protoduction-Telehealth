# Generated by Django 5.0.6 on 2024-06-26 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_consultationrequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='specialty',
            field=models.CharField(default=None, max_length=100),
        ),
    ]
