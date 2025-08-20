from django.db.migrations.executor import MigrationExecutor
from django.db import connections

try:
    connection = connections['DATABASES']
    executor = MigrationExecutor(connection)
    # Pega as migrações aplicadas e as pendentes
    applied_migrations = executor.loader.applied_migrations
    all_migrations = executor.loader.graph.nodes.keys()

    # Diferença indica migrações pendentes
    pending = set(all_migrations) - applied_migrations

    if pending:
        print("Há migrações pendentes:")
        for mig in pending:
            print(mig)
    else:
        print("Todas as migrações estão aplicadas.")
except Exception as e:
    print('Erro', e)
    
