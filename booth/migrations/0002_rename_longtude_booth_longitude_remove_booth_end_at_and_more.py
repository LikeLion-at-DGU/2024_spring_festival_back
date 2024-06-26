# Generated by Django 5.0.4 on 2024-05-21 21:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booth', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='booth',
            old_name='longtude',
            new_name='longitude',
        ),
        migrations.RemoveField(
            model_name='booth',
            name='end_at',
        ),
        migrations.RemoveField(
            model_name='booth',
            name='start_at',
        ),
        migrations.CreateModel(
            name='BoothOperationTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('booth', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='operation_times', to='booth.booth')),
            ],
            options={
                'unique_together': {('booth', 'date')},
            },
        ),
    ]
