# App

#### Estrutura da aplicação:
```bash
.
├── api
│   ├── admin.py                    
│   ├── apps.py
│   ├── __init__.py
│   ├── inventories                 # Diretório para a renderização dos inventories ansible
│   ├── migrations
│   ├── models.py
│   ├── playbooks                   # Diretório para a renderização dos playbooks ansible
│   ├── __pycache__
│   ├── tasks.py                    # Arquivo com toda parte lógica das operações
│   ├── templates                   # Diretório com os templates ansible
│   ├── tests.py
│   ├── urls.py                     # Roteador Django
│   └── views.py                    # Arquivo com as funções de interação dos dispositos para ações na SSoT e da SSoT para interagir com o dispositivos
├── api-entrypoint.sh
├── doc
│   └── contrib
├── docker-compose-local.yml        # Arquivo componente do docker compose
├── docker-compose-registry.yml     # Arquivo componente do docker compose
├── docker-compose.yml              # Arquivo base do docker compose
├── Dockerfile                      # Arquivo declarativo do contêiner docker
├── LICENSE
├── manage.py                       # Arquivo de entrada do Django
├── net2d
│   ├── asgi.py
│   ├── celery.py
│   ├── __init__.py
│   ├── __pycache__
│   ├── settings.py
│   ├── static
│   ├── urls.py
│   └── wsgi.py
├── README.md
├── requirements.txt                # Arquivo de declaração de requisitos do projeto
├── static
│   ├── admin
└── └── rest_framework
```
