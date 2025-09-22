import datetime
import os
import re
import json
# import pandas
import sqlite3

import google.generativeai as genai

from decouple import config

from django.db import connection
from django.db import connections
from django.template import Template, Context
from django.db.migrations.executor import MigrationExecutor
from django.conf import settings

# from utils.extrai_esquemaBD import extrai_esquema_mysql

class Conecta:
    @staticmethod
    def houve_alteracao_banco():
        try:
            connection = connections['default']
            executor = MigrationExecutor(connection)

            # Pega as migrações aplicadas e as pendentes
            applied_migrations = executor.loader.applied_migrations
            all_migrations = executor.loader.graph.nodes.keys()

            # Diferença indica migrações pendentes
            pending = set(all_migrations) - set(applied_migrations)

            if pending:
                print("Há migrações pendentes:")
                for mig in pending:
                    print(mig)
                return True
            else:
                print("Todas as migrações estão aplicadas.")
                return False
        except Exception as e:
            print('Erro', e)
            return False

    @staticmethod
    def conecta_api(): #conecta com api gemini
        # Configura o Gemini API
        try:
            # Verifica se houve alteração pelo migrations
            if Conecta.houve_alteracao_banco():
                Conecta.atualiza_contexto()

            # Configura a chave da API do Gemini
            try:
                api_key = config('GEMINI_API_KEY')
            except:
                api_key = os.getenv('GEMINI_API_KEY')

            if not api_key:
                raise Exception("Chave API do Google não encontrada. Configure GOOGLE_API_KEY nas variáveis de ambiente ou no .env")

            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            return model
        except Exception as e:
            erro = f"Erro de conexão, contate o administrador. \nCódigo: {str(e)}"
            return erro

    @staticmethod
    def atualiza_contexto():
        # Lê o arquivo schema.json para entender o banco de dados
        try:
            schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'schema.json')

            with open(schema_path, "r", encoding='utf-8') as file:
                schema_data = json.load(file)
                return f"Contexto atualizado com sucesso. Schema carregado com {len(schema_data.get('models', {}))} modelos."
        except Exception as e:
            return f"Erro ao atualizar contexto. Exceção: {str(e)}"

    @staticmethod
    def carrega_schema():
        # Carrega o esquema do banco de dados do arquivo schema.json
        try:
            schema_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'schema.json')

            with open(schema_path, "r", encoding='utf-8') as file:
                schema_data = json.load(file)
                return schema_data
        except Exception as e:
            print(f"Erro ao carregar schema: {str(e)}")
            return None

    @staticmethod
    def gera_sql(pergunta):
        try:
            model = Conecta.conecta_api()# conecta com gemini api
            if isinstance(model, str):  # Se retornou erro
                return model

            # Carrega o schema do banco de dados
            schema_data = Conecta.carrega_schema()
            if not schema_data:
                return "Erro ao carregar o esquema do banco de dados."

            # Constrói o prompt com o contexto do schema
            context_prompt = f"""
            Você é um especialista em SQL para Django. Gere UMA consulta SQL válida baseada nas tabelas disponíveis.

            O Schema é:
            {schema_data}

            REGRAS CRÍTICAS:
            1. Retorne APENAS UMA instrução SELECT válida
            2. NÃO use ponto e vírgula (;)
            3. FAÇA SOMENTE SELEÇÃO de dados (SELECT). NÃO use INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, EXEC, MERGE ou TRUNCATE
            4. Para buscar por nome use: WHERE nome LIKE '%parte_do_nome%'
            5. SEMPRE selecione campos completos (ex: u.nome, não SUBSTRING ou similar)
            6. NÃO use funções que dividem strings em caracteres
            7. Máximo 5 colunas no SELECT
            8. Ignore campos padroes do django

            PERGUNTA: {pergunta}

            SQL:
            """

            response = model.generate_content(context_prompt)
            sql_resposta = response.text.strip()

            # Remove possíveis marcadores de código markdown
            if sql_resposta.startswith('```sql'):
                sql_resposta = sql_resposta[6:]
            if sql_resposta.startswith('```'):
                sql_resposta = sql_resposta[3:]
            if sql_resposta.endswith('```'):
                sql_resposta = sql_resposta[:-3]

            # Remove ponto e vírgula no final e quebras de linha extras
            sql_limpo = sql_resposta.strip()
            if sql_limpo.endswith(';'):
                sql_limpo = sql_limpo[:-1]

            # Se houver múltiplas instruções separadas por ';', pega apenas a primeira
            if ';' in sql_limpo:
                sql_limpo = sql_limpo.split(';')[0].strip()

            return sql_limpo
        except Exception as e:
            erro = f"Não foi possível conectar no servidor para gerar a consulta. Por favor, tente novamente mais tarde. Erro: {str(e)}"
            return erro

    @staticmethod
    def checa_consulta_segura(sql): #NAO ALTERAR, REUTILIZAR
        sql = sql.strip().lower()

        # Primeiro, verifica se a consulta começa com SELECT ou WITH
        if not sql.startswith("select") and not sql.startswith("with"):
            return False

        # Segundo, verifica se há ponto e vírgula no meio da consulta
        if ';' in sql:
            parts = [p.strip() for p in sql.split(';') if p.strip()]
            for part in parts:
                if not part.startswith('select') and not part.startswith('with'):
                    return False

        # Por fim, verifica se há palavras-chave potencialmente perigosas
        forbidden = ['insert', 'update', 'delete', 'drop', 'alter', 'create', 'exec', 'merge', 'truncate']
        if any(word in sql for word in forbidden):
            return False

        return True

    @staticmethod
    def executa_sql(sql): #NAO ALTERAR, REUTILIZAR
        try:
            # Verifica se a consulta é segura
            if not Conecta.checa_consulta_segura(sql):
                return "Uma consulta potencialmente insegura foi detectada. Por favor, tente novamente."

            # Conecta no banco com cursor e obtém os resultados
            with connection.cursor() as cursor:
                cursor.execute(sql)
                resultados = cursor.fetchall()

                # Se não houver resultados, retorna a mensagem
                if not resultados:
                    return "Nenhum resultado relevante foi encontrado."

                # Obtém os nomes dos campos
                nomes_campos = [i[0].upper() for i in cursor.description]

            # Verifica se resultados é string (mensagem de erro)
            if isinstance(resultados, str):
                return resultados

            # Se não houver "order by" na consulta, ordena a lista de listas (com proteção)
            if "order by" not in sql.lower() and resultados:
                try:
                    # Verifica se os resultados têm pelo menos um elemento para ordenar
                    if len(resultados) > 0 and len(resultados[0]) > 0:
                        lista_dados = sorted(resultados, key=lambda x: x[0] if x and len(x) > 0 else '')
                    else:
                        lista_dados = resultados
                except (IndexError, TypeError, AttributeError):
                    lista_dados = resultados
            else:
                lista_dados = resultados

            # Filtra os resultados
            lista_filtrada = Conecta.filtra_resultados(lista_dados, nomes_campos)

            if lista_filtrada == 'Erro':
                raise Exception("Mais de 5 colunas retornadas. Por favor, refine sua consulta.")

            # Gera a tabela HTML com os resultados filtrados
            return Conecta.gera_tabela_html(nomes_campos, lista_filtrada)

        except Exception as e:
            return f"Erro na execução da consulta. Erro: {str(e)}. Dúvida, contate o administrador!"

    @staticmethod
    def filtra_resultados(resultados, nomes_campos):
        # Filtra campos indesejados
        campos_indesejados = {'SLUG', 'PASSWORD', 'ARQUIVO_PROJETO'}
        indices_validos = [i for i, nome in enumerate(nomes_campos) if nome not in campos_indesejados]
        nomes_campos = [nomes_campos[i] for i in indices_validos]

        # Se houver mais de 5 colunas, retorna a mensagem
        if len(nomes_campos) > 5:
            return 'Erro'

        # Converte os resultados (tuplas) em uma lista de listas, filtrando os campos indesejados
        lista_dados = [[linha[i] for i in indices_validos] for linha in resultados]

        # Formata os objetos datetime.date/datetime para o formato brasileiro
        for linha in lista_dados:
            for i, valor in enumerate(linha):
                if isinstance(valor, datetime.date):
                    linha[i] = valor.strftime('%d/%m/%Y')
                if isinstance(valor, datetime.datetime):
                    linha[i] = valor.strftime('%d/%m/%Y %H:%M:%S')

        return lista_dados

    @staticmethod
    def gera_tabela_html(nomes_campos, lista_dados):
        template_str = """
                        <h2 style="text-align:center;">Tabela de Resposta</h2>
                        <table class="table table-hover">
                            <thead>
                                <tr>
                                    {% for campo in nomes_campos %}
                                        <th>{{ campo }}</th>
                                    {% endfor %}
                                </tr>
                            </thead>
                            <tbody>
                                {% for item in lista_dados %}
                                    <tr>
                                        {% for valor in item %}
                                            <td>{{ valor }}</td>
                                        {% endfor %}
                                    <tr>
                                {% endfor %}
                            </tbody>
                        </table>
                        <p><b>Total de registros:</b> {{ lista_dados|length }}</p>
                        """
        template = Template(template_str)
        context = Context({
            'nomes_campos': nomes_campos,
            'lista_dados': lista_dados
        })
        return template.render(context)

    #-------------------------------------------------------------------------
