# import datetime
# import pandas
# import sqlite3
# import xmlrpc.client
#
# from decouple import config
#
# from django.db import connection
# from django.db import connections
# from django.template import Template, Context
# from django.db.migrations.executor import MigrationExecutor
#
# from utils.extrai_esquemaBD import extrai_esquema_mysql
#
# class Conecta:
#     @staticmethod
#     def houve_alteracao_banco():
#         try:
#             connection = connections['default']
#             executor = MigrationExecutor(connection)
#
#             # Pega as migrações aplicadas e as pendentes
#             applied_migrations = executor.loader.applied_migrations
#             all_migrations = executor.loader.graph.nodes.keys()
#
#             # Diferença indica migrações pendentes
#             pending = set(all_migrations) - set(applied_migrations)
#
#             if pending:
#                 print("Há migrações pendentes:")
#                 for mig in pending:
#                     print(mig)
#                 return True
#             else:
#                 print("Todas as migrações estão aplicadas.")
#                 return False
#         except Exception as e:
#             print('Erro', e)
#             return False
#
#     @staticmethod
#     def conecta_rpc():
#         # Realiza a conexão com o serivor RPC pela URL.
#         url_servidor = config('GERADORSQL_URL')
#         try:
#             # Verifica se houve alteração pelo migrations
#             if Conecta.houve_alteracao_banco():
#                 Conecta.atualiza_contexto()
#
#             proxy = xmlrpc.client.ServerProxy(url_servidor)
#             return proxy
#         except Exception as e:
#             erro = f"Erro de conexão, contate o administrador. \nCódigo: {str(e)}"
#             return erro
#
#     @staticmethod
#     def atualiza_contexto():
#         # Cria o arquivo JSON pelo método implementado no Utils
#         extrai_esquema_mysql()
#         # Envia o arquivo JSON para o servidor via RPC
#         try:
#             proxy = Conecta.conecta_rpc()
#             with open("esquema_banco.json", "r") as file:
#                 #Lê o arquivo Json e envia para o servidor
#                 json_data = file.read()
#                 resposta = proxy.atualiza_contexto(json_data)
#                 return resposta
#         except Exception as e:
#             return f"Erro ao atualizar contexto. Exceção: {str(e)}"
#
#     @staticmethod
#     def gera_sql(pergunta):
#         try:
#             proxy = Conecta.conecta_rpc()
#             resposta = proxy.gera_resposta(pergunta)
#             return resposta
#         except Exception as e:
#             erro = f"Não foi possível conectar no servidor para gerar a consulta. Por favor, tente novamente mais tarde."
#             return erro
#
#     @staticmethod
#     def checa_consulta_segura(sql):
#         sql = sql.strip().lower()
#
#         # Primeiro, verifica se a consulta começa com SELECT ou WITH
#         if not sql.startswith("select") and not sql.startswith("with"):
#             return False
#
#         # Segundo, verifica se há ponto e vírgula no meio da consulta
#         if ';' in sql:
#             parts = [p.strip() for p in sql.split(';') if p.strip()]
#             for part in parts:
#                 if not part.startswith('select') and not part.startswith('with'):
#                     return False
#
#         # Por fim, verifica se há palavras-chave potencialmente perigosas
#         forbidden = ['insert', 'update', 'delete', 'drop', 'alter', 'create', 'exec', 'merge', 'truncate']
#         if any(word in sql for word in forbidden):
#             return False
#
#         return True
#
#     @staticmethod
#     def executa_sql(sql):
#         try:
#             # Verifica se a consulta é segura
#             if not Conecta.checa_consulta_segura(sql):
#                 return "Uma consulta potencialmente insegura foi detectada. Por favor, tente novamente."
#
#             # Conecta no banco com cursor e obtém os resultados
#             with connection.cursor() as cursor:
#                 cursor.execute(sql)
#                 resultados = cursor.fetchall()
#
#                 # Se não houver resultados, retorna a mensagem
#                 if not resultados:
#                     resultados = "Nenhum resultado relevante foi encontrado."
#
#                 # Obtém os nomes dos campos
#                 nomes_campos = [i[0].upper() for i in cursor.description]
#
#                 cursor.close()
#
#             # Se não houver "order by" na consulta, ordena a lista de listas
#             if "order by" not in sql.lower():
#                 lista_dados = sorted(resultados, key=lambda x: x[0])
#             else:
#                 lista_dados = resultados
#
#             # Filtra os resultados
#             lista_filtrada = Conecta.filtra_resultados(lista_dados, nomes_campos)
#
#             if lista_filtrada == 'Erro':
#                 raise Exception("Mais de 5 colunas retornadas. Por favor, refine sua consulta.")
#
#             # Gera a tabela HTML com os resultados filtrados
#             return Conecta.gera_tabela_html(nomes_campos, lista_filtrada)
#
#         except Exception as e:
#             return f"Erro na execução da consulta. Erro: {str(e)}. Dúvida, contate o administrador!"
#
#     @staticmethod
#     def filtra_resultados(resultados, nomes_campos):
#         # Filtra campos indesejados
#         campos_indesejados = {'SLUG', 'PASSWORD', 'ARQUIVO_PROJETO'}
#         indices_validos = [i for i, nome in enumerate(nomes_campos) if nome not in campos_indesejados]
#         nomes_campos = [nomes_campos[i] for i in indices_validos]
#
#         # Se houver mais de 5 colunas, retorna a mensagem
#         if len(nomes_campos) > 5:
#             return 'Erro'
#
#         # Converte os resultados (tuplas) em uma lista de listas, filtrando os campos indesejados
#         lista_dados = [[linha[i] for i in indices_validos] for linha in resultados]
#
#         # Formata os objetos datetime.date/datetime para o formato brasileiro
#         for linha in lista_dados:
#             for i, valor in enumerate(linha):
#                 if isinstance(valor, datetime.date):
#                     linha[i] = valor.strftime('%d/%m/%Y')
#                 if isinstance(valor, datetime.datetime):
#                     linha[i] = valor.strftime('%d/%m/%Y %H:%M:%S')
#
#         return lista_dados
#
#     @staticmethod
#     def gera_tabela_html(nomes_campos, lista_dados):
#         template_str = """
#                         <h2 style="text-align:center;">Tabela de Resposta</h2>
#                         <table class="table table-hover">
#                             <thead>
#                                 <tr>
#                                     {% for campo in nomes_campos %}
#                                         <th>{{ campo }}</th>
#                                     {% endfor %}
#                                 </tr>
#                             </thead>
#                             <tbody>
#                                 {% for item in lista_dados %}
#                                     <tr>
#                                         {% for valor in item %}
#                                             <td>{{ valor }}</td>
#                                         {% endfor %}
#                                     <tr>
#                                 {% endfor %}
#                             </tbody>
#                         </table>
#                         <p><b>Total de registros:</b> {{ lista_dados|length }}</p>
#                         """
#         template = Template(template_str)
#         context = Context({
#             'nomes_campos': nomes_campos,
#             'lista_dados': lista_dados
#         })
#         return template.render(context)
#
#     #-------------------------------------------------------------------------
#     # metodo do trabalho do Pedro
#     @staticmethod
#     def gera_dataframe():
#         # Conexão com o SQLite
#         conexao = sqlite3.connect('projeto/db.sqlite3')
#         # Query para tabela de usuário
#         consulta_usuario = """
#         SELECT
#             usuario.id AS usuario_id, usuario.nome, usuario.area_conhecimento_cnpq, usuario.curso_graduacao_vinculado,
#             usuario.curso_pos_graduacao, usuario.grupo_pesquisa
#         FROM
#             usuario_usuario as usuario
#         """
#         # Query para tabela de submissao
#         consulta_submissao = """
#         SELECT
#             submissao.edital_id, submissao.responsavel_id, submissao.area, submissao.curso_graduacao_vinculado,
#             submissao.curso_pos_graduacao, submissao.grupo_pesquisa, submissao.titulo, submissao.resumo
#         FROM
#             submissao_submissao AS submissao
#         """
#         # Carrega os dados no pandas DataFrame, para as duas consultas
#         data_frame_usuario = pandas.read_sql_query(consulta_usuario, conexao)
#         data_frame_submissao = pandas.read_sql_query(consulta_submissao, conexao)
#         # Feche a conexão
#         conexao.close()
#         # Mescla os dois DataFrames
#         data_frame_merge = data_frame_submissao.merge(data_frame_usuario, left_on='responsavel_id', right_on='usuario_id', how='left')
#
#         # Colunas do DataFrame mesclado
#         # ['edital_id', 'responsavel_id', 'area', 'curso_graduacao_vinculado_x', 'curso_pos_graduacao_x', 'grupo_pesquisa_x', 'titulo',
#         # 'resumo', 'usuario_id', 'nome', 'area_conhecimento_cnpq', 'curso_graduacao_vinculado_y', 'curso_pos_graduacao_y', 'grupo_pesquisa_y']
#
#         # Seleciona as colunas do descritivo
#         colunas_selecionadas = data_frame_merge[['nome', 'curso_graduacao_vinculado_x', 'titulo', 'curso_graduacao_vinculado_y']]
#         # Retorna o DataFrame
#         return colunas_selecionadas