# Sistema Web de Gestão em Eficiência Energética

## Instalação

> Clone este repositório. Depois de obter o código, abra o terminal e navegue até o diretório do projeto, no código-fonte.

```bash
$ # Clone o projeto
$ git clone https://github.com/Daniel-Fiuza/sistema-gestao-eficiencia-energetica.git
$ cd sistema-gestao-eficiencia-energetica
$
$ # Instalação de módulos no Virtualenv (Sistemas baseados em Unix)
$ virtualenv env
$ source env/bin/activate
$
$ # Instalação de módulos no Virtualenv (Sistemas baseados em Windows)
$ # virtualenv env
$ # .\env\Scripts\activate
$
$ # Instale os módulos necessários
$ pip3 install -r requirements.txt
$
$ # Crie as tabelas
$ python manage.py makemigrations
$ python manage.py migrate
$
$ # Inicie a aplicação
$ python manage.py runserver # default port 8000
$
$ # Inicie a aplicação em uma porta específica
$ # python manage.py runserver 0.0.0.0:<porta>
$
$ # Acesse o aplicativo no navegador: http://127.0.0.1:8000/
```

> OBS: Para usar o aplicativo, acesse a página de registro e crie um novo usuário. Após a autenticação, o aplicativo irá desbloquear as páginas protegidas.

<br />

## Documentação da Biblioteca
A documentação se encontra no [website](https://demos.creative-tim.com/argon-dashboard-django/docs/getting-started/getting-started-django.html).

<br />

## Estrutura do Código Base

O projeto foi codificado utilizando a estrutura apresentada abaixo:

```bash
< PROJECT ROOT >
   |
   |-- core/                               # Implements app configuration
   |    |-- settings.py                    # Defines Global Settings
   |    |-- wsgi.py                        # Start the app in production
   |    |-- urls.py                        # Define URLs served by all apps/nodes
   |
   |-- apps/
   |    |
   |    |-- home/                          # A simple app that serve HTML files
   |    |    |-- views.py                  # Serve HTML pages for authenticated users
   |    |    |-- urls.py                   # Define some super simple routes  
   |    |
   |    |-- authentication/                # Handles auth routes (login and register)
   |    |    |-- urls.py                   # Define authentication routes  
   |    |    |-- views.py                  # Handles login and registration  
   |    |    |-- forms.py                  # Define auth forms (login and register) 
   |    |
   |    |-- static/
   |    |    |-- <css, JS, images>         # CSS files, Javascripts files
   |    |
   |    |-- templates/                     # Templates used to render pages
   |         |-- includes/                 # HTML chunks and components
   |         |    |-- navigation.html      # Top menu component
   |         |    |-- sidebar.html         # Sidebar component
   |         |    |-- footer.html          # App Footer
   |         |    |-- scripts.html         # Scripts common to all pages
   |         |
   |         |-- layouts/                   # Master pages
   |         |    |-- base-fullscreen.html  # Used by Authentication pages
   |         |    |-- base.html             # Used by common pages
   |         |
   |         |-- accounts/                  # Authentication pages
   |         |    |-- login.html            # Login page
   |         |    |-- register.html         # Register page
   |         |
   |         |-- home/                      # UI Kit Pages
   |              |-- index.html            # Index page
   |              |-- 404-page.html         # 404 page
   |              |-- *.html                # All other pages
   |
   |-- requirements.txt                     # Development modules - SQLite storage
   |
   |-- .env                                 # Inject Configuration via Environment
   |-- manage.py                            # Start the app - Django default start script
   |
   |-- ************************************************************************
```

<br />

> Fluxo de inicialização

- A arquivo de inicialização do Django `manage.py` utiliza `core/settings.py` como principal arquivo de configuração
- `core/settings.py` carrega o app com o arquivo `.env`
- Redirecione os usuários convidados para a página de login
- Desbloqueie as páginas servidas pelo dentro de *app* para usuários autenticados

<br />

## Implementação (Deployment)

O app apresenta uma configuração básica para ser executado no [Docker](https://www.docker.com/), [Gunicorn](https://gunicorn.org/), e [Waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/).

### Execução no [Docker](https://www.docker.com/)
---

A aplicação pode ser facilmentes executada em containeres. Seguem os passos:

> Obtenha o código

```bash
$ git clone https://github.com/Daniel-Fiuza/sistema-gestao-eficiencia-energetica.git
$ cd sistema-gestao-eficiencia-energetica
```

> Inicie o app no Docker

```bash
$ sudo docker-compose pull && sudo docker-compose build && sudo docker-compose up -d
```

Visite `http://localhost:85` no seu navegador. O aplicativo deve estar em execução.

<br />

## Navegadores Suportados

No momento, o sistema suporta as últimas versões dos seguintes navegadores:

<img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/chrome.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/firefox.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/edge.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/safari.png" width="64" height="64"> <img src="https://s3.amazonaws.com/creativetim_bucket/github/browser/opera.png" width="64" height="64">

<br />