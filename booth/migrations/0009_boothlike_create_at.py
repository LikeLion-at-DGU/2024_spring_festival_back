# Generated by Django 5.0.4 on 2024-05-27 12:38

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booth', '0008_alter_comment_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='boothlike',
            name='create_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
