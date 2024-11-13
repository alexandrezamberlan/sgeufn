# Disponibilizando no servidor Linux

## Necessidade de serviços instalados:
    1) nginx
    2) gunicorn
    3) mysql
    4) ssh liberado
    5) python
    6) git

## Primeiros passos:
    1) acessar o servidor via ssh
    2) criar a pasta para receber o repositório
        - Políticas ou boas práticas da Infraestrutura UFN
            1) sistemas web devem estar em /var/www
            2) nome da pasta do sistema deve ser sgeufn.lapinf.ufn.edu.br
    3) clonar o projeto do github no servidor
    4) criar a venv
        - usar virtualenv: virtualenv -p python3.10 venv (exceção pq o servidor contém o python 2.7)
    5) ativar venv
        - source venv/bin/activate (exceção pq é um servidor linux)
    6) instalar pacotes

## Passos de configuração

### GUNICORN 

    - criar o arquivo /etc/systemd/system/sgeufn.service

```
[Unit]
Description=sgeufn daemon
After=network.target

[Service]
User=alexz
Group=www-data
WorkingDirectory=/var/www/sgeufn.lapinf.ufn.edu.br/sgeufn/projeto
ExecStart=/var/www/sgeufn.lapinf.ufn.edu.br/sgeufn/venv/bin/gunicorn --access-logfile - --workers 3 --bind unix:/var/www/sgeufn.lapinf.ufn.edu.br/sgeufn/projeto/sgeufn.sock projeto.wsgi:application
```

    - iniciar o parser gunicorn:
        - sudo systemctl start sgeufn

    - adicionar o sistema como serviço reconhecido no sistema:
        - sudo systemctl enable sgeufn


### NGINX
 
Para que o Nginx sirva esse conteúdo, é necessário criar um bloco de servidor com as diretivas corretas. 
Em vez de modificar o arquivo de configuração padrão diretamente, vamos criar um novo em 

    - /etc/nginx/sites-available/sgeufn.lapinf.ufn.edu.br
 
    - sudo vim /etc/nginx/sites-available/sgeufn.lapinf.ufn.edu.br


Cole dentro o seguinte bloco de configuração, que é similar ao padrão, mas atualizado para nosso novo diretório e nome de domínio:
 
```
server {
        server_name sgeufn.lapinf.ufn.edu.br www.sgeufn.lapinf.ufn.edu.br;
        client_body_in_file_only clean;
        client_body_buffer_size 32K;
        client_max_body_size 2512M;

        #aceitar arquivos grande via get
        client_header_buffer_size 3232k;
        large_client_header_buffers 4 3232k;
        sendfile on;
        send_timeout 900s;
        location = /favicon.ico { access_log off; log_not_found off; }

        location /static {
                expires 30d;
                access_log off;
                break;
                alias /var/www/sgeufn.lapinf.ufn.edu.br/sgeufn/projeto/projeto/static;
        }

        location / {
                client_max_body_size 2048M;
                include proxy_params;
                proxy_pass http://unix:/var/www/sgeufn.lapinf.ufn.edu.br/sgeufn/projeto/sgeufn.sock;
        }
} 
```

Observe que atualizamos a configuração root para corresponder ao nosso novo diretório e 
server_name ao nosso nome de domínio. A seguir, vamos ativar o arquivo através da criação de um link dele para o diretório sites-enabled, a partir do qual o Nginx lê durante a inicialização:
 
    - sudo ln -s /etc/nginx/sites-available/sgeufn.lapinf.ufn.edu.br /etc/nginx/sites-enabled/
 
Depois, teste para certificar-se de que não existem erros de sintaxe em quaisquer de seus arquivos do Nginx:
 
    - sudo nginx -t


Salve e feche o arquivo quando tiver terminado. Se não houver problemas, reinicie o Nginx para ativar suas alterações:
 
    - sudo systemctl restart nginx


### Obtendo um Certificado SSL
 
    - sudo certbot --nginx -d sgeufn.lapinf.ufn.edu.br -d www.sgeufn.lapinf.ufn.edu.br
 
Se isso for bem sucedido, o certbot perguntará como você gostaria de definir suas configurações de HTTPS. Usa 2 para sempre redirecionar para SSL

```
Output
Please choose whether or not to redirect HTTP traffic to HTTPS, removing HTTP access.
-------------------------------------------------------------------------------
1: No redirect - Make no further changes to the webserver configuration.
2: Redirect - Make all requests redirect to secure HTTPS access. Choose this for
new sites, or if you're confident your site works on HTTPS. You can undo this
change by editing your web server's configuration.
-------------------------------------------------------------------------------
Select the appropriate number [1-2] then [enter] (press 'c' to cancel):
Selecione a sua escolha e pressione ENTER. A configuração será atualizada, e o Nginx irá recarregar para pegar as novas configurações. O certbot irá terminar com uma mensagem informando que o processo foi bem-sucedido e onde os seus certificados estão armazenados:
 
Output
IMPORTANT NOTES:
- Congratulations! Your certificate and chain have been saved at:
   /etc/letsencrypt/live/exemplo.com/fullchain.pem
   Your key file has been saved at:
   /etc/letsencrypt/live/exemplo.com/privkey.pem
   Your cert will expire on 2018-07-23. To obtain a new or tweaked
   version of this certificate in the future, simply run certbot again
   with the "certonly" option. To non-interactively renew *all* of
   your certificates, run "certbot renew"
- Your account credentials have been saved in your Certbot
   configuration directory at /etc/letsencrypt. You should make a
   secure backup of this folder now. This configuration directory will
   also contain certificates and private keys obtained by Certbot so
   making regular backups of this folder is ideal.
- If you like Certbot, please consider supporting our work by:
 
   Donating to ISRG / Let's Encrypt:   https://letsencrypt.org/donate
   Donating to EFF:                    https://eff.org/donate-le
 
```

### Criando esquema de BD no MYSQL

PARA VISUALIZAR, SE NECESSÁRIO, OS USUÁRIOS DO MYSQL:
    - SELECT user FROM mysql.user;

    - CREATE DATABASE sgeufn_db;

    - CREATE USER 'sgeufn'@'localhost' IDENTIFIED BY 'senhaDesejada';

    - GRANT ALL PRIVILEGES ON sgeufn_db.* TO 'sgeufn'@'localhost' IDENTIFIED BY 'senhaDesejada';

### Rodar migrates

### Criando primeiro usuário

Na pasta projeto do sistema, com a venv ativa, rodar shell

    - python projeto/manage.py shell

```
from usuario.models import Usuario
u = Usuario()
u.nome = 'Nome do Usuario'
u.tipo = 'ADMINISTRADOR'
u.email = 'projetos@ufn.edu.br'
u.is_active = True
u.cpf = '99999999999'
u.save()
u.set_password('projetos@ufn.edu.br')
u.save()
```


### Configurar .env o driver do MYSQL

No arquivo .env adicionar:

    - DATABASE_URL=mysql://sgeufn:senhaEscolhida$@127.0.0.1:3306/sgeufn_db




