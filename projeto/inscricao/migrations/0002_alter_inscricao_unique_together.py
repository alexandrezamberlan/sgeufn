# Generated by Django 5.1.7 on 2025-05-21 16:20

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('evento', '0010_evento_lotacao'),
        ('inscricao', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='inscricao',
            unique_together={('participante', 'evento')},
        ),
    ]
