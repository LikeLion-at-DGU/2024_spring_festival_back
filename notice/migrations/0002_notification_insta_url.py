# Generated by Django 5.0.4 on 2024-05-24 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='insta_url',
            field=models.URLField(blank=True, null=True),
        ),
    ]
