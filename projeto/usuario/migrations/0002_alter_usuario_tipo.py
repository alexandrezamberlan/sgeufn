# Generated by Django 4.2.16 on 2024-11-27 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='tipo',
            field=models.CharField(choices=[('ADMINISTRADOR', 'Administrador'), ('COORDENADOR', 'Coordenador de Evento'), ('PARTICIPANTE', 'Participante')], default='MEMBRO', help_text='* Campos obrigatórios', max_length=15, verbose_name='Tipo do usuário *'),
        ),
    ]