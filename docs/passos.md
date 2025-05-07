# Passos para projeto, implementação e disponibilização de um sistema Web Python-Django

## Criação do repositório ou projeto no GitHub
Uma vez com conta no GitHub, criar repositório ou projeto. Criar README, gitignore, visibilidade, licença e adicionar colaboradores.

## Modelagem do sistema

    1) caso o repositório não esteja na máquina local: 
        1) clona-lo; 
            git clone <enderecoRepositorio>

        2) criar venv; 
            # a partir do python 3.10
            python -m venv venv

        3) instalar requirements.txt
            python -m pip install --upgrade pip
            python -m pip install -r requirements.txt

        4) criar .env com variáveis de ambiente


    2) caso o repositório exista na máquina local (de trabalho): 
        i) realizar um pull

    3) levantar o servidor
        python projeto/manage.py runserver

    4) codificar

    5) realizar o push
        git add .
        git commit -m "mensagem do que foi feito"
        git push

### Criação de venv
    1) atualizar o pip: python -m pip install --upgrade pip
    2) criar a venv:    python -m venv venv
    3) ativar a venv:   venv\Scripts\activate
    4) instalar requirements.txt: python -m pip install -r requirements.txt