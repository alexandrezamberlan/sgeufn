# Sistema de Gestão de Eventos da UFN - SGEUFN
Sistema Web Python-Django que gerencia eventos da Universidade Franciscana, controlando inscrições, presenças e gerando atestados.

Este projeto faz parte do Laboratório de Práticas da Computação UFN, em que alunos dos cursos da área de Computação podem praticar o desenvolvimento de sistema Web Python-Django.

## Integrantes
    - Camille Rodrigues - Sistemas de Informação
    - Bruno Difante - Ciência da Computação
    - Gabriel Morais - Ciência da Computação
    - Pedro Canabarro - Ciência da Computação

## Estruturação

- apps
    - usuario
        - (OK)tipos: administrador, coordenador de evento, participante
        - (OK)nome
        - (OK)email (chave primária)
        - (OK)celular
        - (OK)cpf
        - (OK)instituição (não tem vinculo com app instituição) - pedir pra não usar sigla
        - FOTO PERFIL
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
        - total de inscritos e vagas restantes ??? property
        - (OK)data do evento
        - (OK)coordenador do evento (relação com app usuario) - DEVE SER TIPO COORDENADOR EM USUÁRIO
        - pedir frequencia na entrada (boolean)
        - pedir frequencia na saida (boolean)
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
        - evento
        - inscricao via codigo_matricula (DIGITADO OU LIDO POR QRCODE) OU reconhecimento facial (relação com app inscrição)
        - se o usuário fizer frequencia pelo app, puxar a localização e bater com a localização do evento
        

    - atestado
        - evento (nome, tipo, carga horária (total ou real), instituição, local, data, coordenador do evento (nome e de assinatura))
        - número do atestado
        - enviar por email
        - reenviar por email
        

## Sugestões de CSS
    - https://bootswatch.com/3/
    - Icons bootstrap 
        - https://www.w3schools.com/icons/bootstrap_icons_glyphicons.asp

## .env

SECRET_KEY='aoabb!bk-g5s0uk49ecc#%3#3+is(&3+)@ny%3yo0ct0481q43'

DEBUG=True

STATIC_URL=/static/

DOMINIO_URL='localhost:8000'

EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_HOST_USER = ''

EMAIL_HOST_PASSWORD = ''

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_USE_SSL = False

EMAIL_USE_STARTTLS = False
