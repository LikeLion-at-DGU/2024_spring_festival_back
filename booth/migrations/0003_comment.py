# Generated by Django 5.0.4 on 2024-05-22 21:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booth', '0002_rename_longtude_booth_longitude_remove_booth_end_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('writer', models.CharField(max_length=20)),
                ('content', models.TextField()),
                ('password', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('booth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='booth.booth')),
            ],
        ),
    ]
