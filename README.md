# Sistema de Gestão de Eventos da UFN - SGEUFN

Sistema Web Python-Django que gerencia eventos da Universidade Franciscana, controlando inscrições, presenças e gerando atestados.

## Registro INPI: BR512025003008-8

Este projeto faz parte do Laboratório de Práticas da Computação UFN, em que alunos dos cursos da área de Computação podem praticar o desenvolvimento de sistema Web Python-Django.

## Integrantes
    - Camille Rodrigues - Sistemas de Informação
    - Bruno Difante - Ciência da Computação
    - Gabriel Morais - Ciência da Computação
    - Guilherme Henriques - Ciência da Computação
    - Guilherme Scher - Ciência da Computação
    - Pedro Canabarro - Ciência da Computação

    - Professora Ana Paula Canal
    - Professor Ricardo Frohlich da Silva
    - Professor Sylvio Vieira

    - Consultor da Empresa parceira ER Clinic - Robertson Ebling dos Santos

## Estruturação

- apps
    - usuario
        - (OK)tipos: administrador, coordenador de evento, participante
        - (OK)nome
        - (OK)email (chave primária)
        - (OK)celular
        - (OK)cpf
        - (OK)instituição (não tem vinculo com app instituição) - pedir pra não usar sigla
        - FOTO PERFIL ????
        - (OK)is_active
        - (OK)slug

        Obs.:
            - (OK)usuário faz autocadastro (exceto administrador)
                - (OK)colocar campo de aceite dos termos de uso
                - verificar se está mandando por email a ativação do usuário
    
    - (OK)instituição
        - (OK)nome
        - (OK)sigla (opcional)
        - (OK)cidade
        - (OK)estado
        - (OK)país
        - (OK)is_active
        - (OK)slug

    - evento 
        - (OK)nome ou título
        - (OK)tipo (relação com app tipo de evento - palestra, minicurso, sarau, ...)
        - (OK)carga horária
        - (OK)instituição (relação com app instituição)
        - (OK)local (descrição completa - textfield)
        - (OK)lotação
        - (OK)total de inscritos e vagas restantes ??? property
        - (OK)data do evento
        - (OK)coordenador do evento (relação com app usuario) - DEVE SER TIPO COORDENADOR EM USUÁRIO
        - (OK)is_active
        - (OK)slug
        
    - inscricao
        - (OK)usuário do tipo participante - SE O PARTICIPANTE SE LOGA, É AUTOMATICO A ESCOLHA DO PARTICIPANTE
        - (OK)evento (relação com app evento)
        - (OK)data e hora da inscrição (capturado automático)
        - (OK)codigo_matricula (enviado por email)
        - (OK)is_active
        - (OK)slug

    - frequencia
        - (OK)evento
        - (OK)inscricao via codigo_matricula (DIGITADO OU LIDO POR QRCODE) OU reconhecimento facial (relação com app inscrição)        

    - atestado
        - (OK)evento (nome, tipo, carga horária (total ou real), instituição, local, data, coordenador do evento (nome e de assinatura))
        - (OK)número do atestado

## Sugestões de CSS
    - https://bootswatch.com/3/
    - Icons bootstrap 
        - https://www.w3schools.com/icons/bootstrap_icons_glyphicons.asp

## .env
```
SECRET_KEY='aoabb!bk-g5s0uk49ecc#%3#3+is(&3+)@ny%3yo0ct0481q43'

DEBUG=True

STATIC_URL=/static/

DOMINIO_URL='http://localhost:8000'
GERADORSQL_URL=''

EMAIL_HOST_USER = ''
EMAIL_BACKEND='gmailapi_backend.mail.GmailBackend'
GMAIL_API_CLIENT_ID=''
GMAIL_API_CLIENT_SECRET=''
GMAIL_API_REFRESH_TOKEN=''
EMAIL_REPLY_TO = ''
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
EMAIL_USE_STARTTLS = False
GEMINI_API_KEY = ''
```