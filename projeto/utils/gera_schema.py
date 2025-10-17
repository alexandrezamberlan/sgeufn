import os
import sys
import json
import django

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projeto.settings')
django.setup()

from django.apps import apps
from django.db import models

# Dentro do /projeto para gerar o schema do bd coloque no cmd "python -m utils.gera_schema"

def gerar_schema():
    schema = {}
    all_models = apps.get_models()

    for model in all_models:
        app_label = model._meta.app_label
        model_name = model._meta.model_name
        key = f"{app_label}_{model_name}"

        model_fields = {}
        for field in model._meta.get_fields():
            if not isinstance(field, (models.Field, models.ManyToOneRel, models.ManyToManyRel, models.OneToOneRel)):
                continue

            if hasattr(field, 'auto_created') and field.auto_created:
                continue

            field_name = field.name

            if isinstance(field, (models.ForeignKey, models.OneToOneField, models.ManyToManyField)):
                related_model = field.related_model
                related_model_name = f"{related_model._meta.app_label.capitalize()}{related_model._meta.object_name.capitalize()}"
                field_str = f"{field.__class__.__name__}({related_model_name})"
            else:
                _name, _path, args, kwargs = field.deconstruct()
                params = []
                if args:
                    params.extend(map(str, args))
                if kwargs:
                    if 'max_length' in kwargs:
                        params.append(str(kwargs['max_length']))
                    if 'unique' in kwargs and kwargs['unique']:
                        params.append('unique')
                    if 'max_digits' in kwargs and 'decimal_places' in kwargs:
                        params.append(f"{kwargs['max_digits']},{kwargs['decimal_places']}")

                if params:
                    field_str = f"{field.__class__.__name__}({', '.join(params)})"
                else:
                    field_str = field.__class__.__name__

            model_fields[field_name] = field_str

        if model_fields:
            schema[key] = model_fields

    with open('schema_gerado.json', 'w', encoding='utf-8') as f:
        json.dump(schema, f, indent=4, ensure_ascii=False)

    print('Arquivo schema_gerado.json gerado com sucesso.')


if __name__ == '__main__':
    gerar_schema()