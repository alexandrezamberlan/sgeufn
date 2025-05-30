# Generated by Django 5.1.7 on 2025-05-07 17:07

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('evento', '0010_evento_lotacao'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Inscricao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_hora_inscricao', models.DateTimeField(auto_now_add=True)),
                ('codigo_matricula', models.CharField(max_length=20, verbose_name='Código matrícula gerado por hash *')),
                ('is_active', models.BooleanField(default=True, help_text='Se ativo, a inscrição pode ser usada no sistema', verbose_name='Ativo')),
                ('slug', models.SlugField(blank=True, max_length=200, null=True, verbose_name='Hash')),
                ('evento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='evento', to='evento.evento', verbose_name='Evento da inscrição *')),
                ('participante', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='participante', to=settings.AUTH_USER_MODEL, verbose_name='Inscrito no evento *')),
            ],
            options={
                'verbose_name': 'inscrição',
                'verbose_name_plural': 'inscrições',
                'ordering': ['-is_active', 'evento', 'participante'],
            },
        ),
    ]
