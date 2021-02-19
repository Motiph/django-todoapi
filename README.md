# ToDo con django/djangorestframework

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

password mypassword
https://appname.herokuapp.com/admin


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
    "access_token": "53f9183837695b339e08cf017394fe47a3544917"
}

```

<br />

**ENDPOINTS**

Todo lo siguente APLICA tambien al ambiente local, la base de datos en la nube se encuentra actulamente vacia.

Para cada una de las siguientes peticiones es necesario enviar el token autorizacion en los headers

```
{"Authorization":  "Token 53f9183837695b339e08cf017394fe47a3544917"}
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

**GET** https://django-todoapi.herokuapp.com/api/todos/search?q=CADENADEBUSQUEDA