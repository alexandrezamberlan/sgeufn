# Passos para projeto, implementação e disponibilização de um sistema Web Python-Django

## Criação do repositório ou projeto no GitHub
Uma vez com conta no GitHub, criar repositório ou projeto. Criar README, gitignore, visibilidade, licença e adicionar colaboradores.

## Modelagem do sistema

    1) caso o repositório não esteja na máquina local: 
        1) clona-lo; 
        2) criar venv; 
        3) instalar requirements.txt

    2) caso o repositório exista na máquina local (de trabalho): i) realizar um pull

    3) modelar o sistema e documenta-lo na ferramenta preferida

    4) salvar na pasta DOCS do repositório

    5) realizar o push

### Criação de venv
    1) atualizar o pip: python -m pip install --upgrade pip
    2) criar a venv:    python -m venv venv
    3) ativar a venv:   venv\Scripts\activate
    4) instalar requirements.txt: python -m pip install -r requirements.txt