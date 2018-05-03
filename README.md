SISTEMA DE GESTIÓN COORPORATIVO FINANCIERO
==========================================================

Proyecto desarrollado para la generación de roles de pago en la empresa Minera El Malecón

Módulos
-------
- Master
- Seguridad
- Nominas

Requisitos
----------
1. Instalar los siguientes paquetes de forma global.
    
    ```
    sudo apt-get install python3.6
    sudo apt-get install python-dev libffi-dev libssl-dev libxml2-dev libxslt1-dev
    sudo apt-get install python-dev python-pip python-lxml libcairo2 libpango1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info
    sudo apt-get install libpq-dev
    sudo apt-get install nodejs
    sudo apt-get install npm
    npm install -g @angular/cli
    ```

2. Crear una BD:
   
    ```
    nombre: sigecoraf
    usuario: sigecoraf
    clave: admin
    ```

3. Instalar un entorno virtual para la ejeción del backend del proyecto siaaf.

Instalación Frontend
-----------

1. Instalar los paquetes detallados en el package.json. Ejecutar el comando desde
la raiz del proyecto sigecoraf-web:
    
    ```
    npm install
    ```

Instalación Backend
-----------
1. Activar en entorno virtual y posterior acceder a la carpeta siaaf. Este paso es 
esencial para los pasos posteriores:
    
    ```
    source directorio-entorno-virtual/bin/activate
    ```
    
2. Instalar paquetes necesarios para el backend del proyecto detallados en el archivo requerimientos_pip.txt:
    
    ```
    pip install -r requerimientos_pip
    ```

3. Ejecutamos los archivos estaticos del Django:
    
    ```
    python manage.py collectstatic
    ```

4. Inicializamos las migraciones en la BD con el ORM de Django:
    
    ```
    python manage.py makemigrations
    python migrate
    ```


2. Si el caso lo requiere para crear los tokens, ejecutar la siguiente instrucción para cada usuario.
   
    ```
    Token.objects.create(user=user)
    ```

Levantar aplicación para desarrollo
------------------------

1. Activar en entorno virtual
   
    ```
   source directorio-entorno-virtual/bin/activate
   ```

2. Levantar django. El manage.py utiliza por defecto el **sigecoraf/settings/development.py** donde
estan los datos de conección a la BD
   
    ```
    python manage.py runserver
    ```
   
    Si el caso lo requiere, ejecutar con un settings específico
   
    ```
    python manage.py runserver --settings=sigecoraf.settings.production
    ```
   
3. Desde el directorio de sigecoraf-web, levantar angular
   
    ```
    ng serve
    ```



Levantar aplicación para producción
-------
**Le levanta la aplicación con GUNICORN y NGINX tanto el backend y frontend con https**

1. Generar certificados dentro del directorio de nginx
   
    ```
    /etc/nginx/ssl/server.crt
    /etc/nginx/ssl/server.key
    ```
2. En la ruta de aplicacion de nginx sites-available, crear un archivo de configuración ejemplo sigecoraf.conf:
   
    ```
    /etc/nginx/sites-available/sigecoraf.conf
    ```

3. Crear un enlace simbólico del sigecoraf.conf en el directorio sites-enabled:
   
    ```
    /etc/nginx/sites-enabled/sigecoraf.conf
    ```
    
4. En el archivo sigecoraf.conf configurar para que la parte static de Django y Angular se ejecuten desde nginx con https
 
    ***Ejemplo acceso por URL***
    ```
    Django: https://dominio:8091
    Angular: https://dominio
    ```
    ***Configuración***
    ```
    # DJANGO SIAAF
    server {
        listen 8091 default ssl;
        server_name sigecoraf.com;
        client_max_body_size 4G;
    
        ssl on;
        ssl_certificate /etc/nginx/ssl/server.crt;
        ssl_certificate_key /etc/nginx/ssl/server.key;
    
        location /static/ {
            alias /ruta-proyecto/sigecoraf/staticfiles/;
        }
    
        location / {
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header Host $http_host;
            proxy_redirect off;
            if (!-f $request_filename) {
                #EJECUTADO POR GUNICORN
                proxy_pass http://dominio:8000;
                break;
            }
        }
    }
    
    # ANGULAR SIAAF
    server {
        listen 443;
        server_name  dominio;
    
        ssl on;
        ssl_certificate /etc/nginx/ssl/server.crt;
        ssl_certificate_key /etc/nginx/ssl/server.key;
    
        location / {
            root   /ruta-proyecto/sigecoraf-web;
            index  index.html;
            try_files $uri /index.html;
        }
    }
    ```

5. Activar el entorno virtual y levantar la aplicación de Django con gunicorn. Para producción se
utiliza el wsgi que hace referencia al archivo **siaa/settings/production.py** donde estan los
datos de conección a la BD.
    
    ***Crear el archivo siaa/settings/production.py y modificar los datos según sea necesario***
    ```
    from .base import *
    DEBUG = False
    ALLOWED_HOSTS = ['*']
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'sigecoraf',
            'USER': 'sigecoraf',
            'PASSWORD': 'admin',
            'HOST': 'localhost',
            'PORT': '5432',
        }
    }
    ```
    
    ***Levantar django con gunicorn***
    ```
    gunicorn sigecoraf.wsgi:application --bind dominio:8000
    ```
6. Acceder a las urls del proyecto del BANCKEND (django) y FRONTEND (angular.io).
    ```
    Backend: https://dominio:8091
    Frontend: https://dominio
    ```

Levantar aplicación con SSL para django
---

1. Verificar que estén en:

    ```
    INSTALLED_APPS = (
        …
        ‘djangosecure’,
        ‘sslserver’
        …
    )
    ```
    
2. Levantar el servidor con los certificados previamente ya creados.
 
    ```
    python manage.py runsslserver --cert /etc/nginx/ssl/server.crt --key /etc/nginx/ssl/server.key
    ```
