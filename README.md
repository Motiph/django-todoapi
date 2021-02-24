# ToDo/Tasks con django/djangorestframework

<br />

## **Local con Dockerfile**

```
cd django-todoapi
```

Creamos la imagen

```
docker build -t django-todoapi:v1 .
```

Arrancamos el contendor y probamos la app
```
docker run -p 8000:8000 django-todoapi:v1
```

username admin

password mypassword

http://localhost:8000/admin/


<br />


## **Local con virtualenv**
```
mkvirtualenv todo
workon todo
cd django-todoapi
pip install -r requirements.txt
python manage.py runserver --settings=todo.settings.local
```

username admin

password mypassword
http://localhost:8000/admin/


**TESTS**

```
python manage.py test apps.core.tests --settings=todo.settings.local
```


<br />

## **Deploy en Heroku**



Es necesario tener instalado Heroku CLI

Editamos el DockerFile y lo dejamos de estar forma
```
#Local
#EXPOSE 8000

#CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "todo.wsgi:application"]

#Este es para heroku ya que no te permite exponer el puerto.
CMD gunicorn todo.wsgi:application --bind 0.0.0.0:$PORT
```

<br />

Login
```
cd django-todoapi
heroku container:login
```

Creamos la app
```
heroku create appname
```

Creamos una imagen especifica para tabajar con heroku y docker
```
heroku push container:push web -a=appname
```

Configuramos variables (opcional, tambien se puede hacer manual desde el dashboard de heroku)
```
heroku config:add ALLOWED_HOST=* -a appname
heroku config:add SECRET_KEY=SECRET -a appname
heroku config:add DEBUG=False -a appname
```

Liberamos la app
```
heroku container:release -a appname web
```
username admin

password mypassword123
https://appname.herokuapp.com/admin


**NOTA**: No es no necesario ejecutar python manage.py collectstatic ya que se creó un storage en AWS para las peticiones de los static files 

<br />

# Funcionamiento

usuario admin

password mypassword123

**Endpoint** https://django-todoapi.herokuapp.com/

<br />

Es necesario iniciar sesion para obtener un token y realizar todas las otras peticiones




```
https://django-todoapi.herokuapp.com/api/login/

request

{
    "username": "admin",
    "password": "mypassword123"
}

response

{
    "access_token": "6369269c9ee86566b751919d91f8ddb36d2c16ee"
}

```

<br />

**ENDPOINTS**

Todo lo siguente APLICA tambien al ambiente local, la base de datos en la nube se encuentra actulamente vacia.

Para cada una de las siguientes peticiones es necesario enviar el token autorizacion en los headers

```
{"Authorization":  "Token 6369269c9ee86566b751919d91f8ddb36d2c16ee"}
```


1 - Para llenar la base de datos vamos a crear tareas aleatorias deacuerdo al requisito

1.1 **GET** https://django-todoapi.herokuapp.com/api/makejson/ 

<br />

2 - Enviaremos el response del endpoint #1 al siguiente endpoint para crear las tareas

2.1 - **POST** https://django-todoapi.herokuapp.com/api/todos/create/list

<br />

3 - Lista toda las tareas y puede regresar XML y JSON dependiendo el request

3.1 - **GET** https://django-todoapi.herokuapp.com/api/todos/ 


<br />


**Crear una tarea**

**POST** https://django-todoapi.herokuapp.com/api/create
```
{
    "description": "Crear Api",
    "duration": 30,
    "status":  "Pendiente"
}
```

<br />

**Actualizar una tarea(completar)**

**PUT** https://django-todoapi.herokuapp.com/api/todos/{id}/update

```
{
    "description": "Crear Api",
    "duration": 60,
    "status": "Completada",
    "recorded_time": 60
}
```

<br />


**Eliminar una tarea**

**DELETE** https://django-todoapi.herokuapp.com/api/todos/{id}/delete

<br />

**Peticion para una tarea en especifico**

**GET** https://django-todoapi.herokuapp.com/api/todos/{id} 

<br />

**Filtrar Tareas por status "pendiente/completada"**

Puede regresar XML y JSON dependiendo el request

**GET** https://django-todoapi.herokuapp.com/api/todos/status?q=pendiente

**GET** https://django-todoapi.herokuapp.com/api/todos/status?q=completada


<br />

**Obtener las tareas cuya descripción incluya con una cadena de búsqueda**
Puede regresar XML y JSON dependiendo el request

**GET** https://django-todoapi.herokuapp.com/api/todos/search?q=CADENADEBUSQUEDA
