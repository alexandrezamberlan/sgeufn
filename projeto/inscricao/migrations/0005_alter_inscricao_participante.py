# Generated by Django 4.2.21 on 2025-05-30 11:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inscricao', '0004_alter_inscricao_participante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inscricao',
            name='participante',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='participante', to=settings.AUTH_USER_MODEL, verbose_name='Participante'),
        ),
    ]
