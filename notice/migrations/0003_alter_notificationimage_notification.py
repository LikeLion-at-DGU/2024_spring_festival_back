# Generated by Django 5.0.4 on 2024-05-25 01:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notice', '0002_notification_insta_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notificationimage',
            name='notification',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='notice.notification'),
        ),
    ]
