# Generated by Django 5.1.2 on 2024-10-15 17:14

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_initial'),
        ('social', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='review',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='reviews.review'),
        ),
    ]