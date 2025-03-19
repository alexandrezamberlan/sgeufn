# Generated by Django 5.1.7 on 2025-03-19 16:44

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('evento', '0007_evento_lotacao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='evento',
            name='lotacao',
            field=models.DecimalField(blank=True, decimal_places=0, max_digits=4, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(12)], verbose_name='Lotação máxima do local do evento '),
        ),
    ]
