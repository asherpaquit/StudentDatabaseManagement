# Generated by Django 5.1.1 on 2024-10-13 15:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sdm', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='student',
            name='password',
            field=models.CharField(default='12345', max_length=128),
            preserve_default=False,
        ),
    ]
