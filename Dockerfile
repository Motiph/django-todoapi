# Python y Linux
FROM python:3.10.0a1-alpine3.12

COPY requirements.txt /app/requirements.txt

# Servidor
RUN set -ex \
    && pip install --upgrade pip \  
    && pip install --no-cache-dir -r /app/requirements.txt 

# Directorio
WORKDIR /app

ADD . .

# Local
EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "todo.wsgi:application"]

#Este es para heroku ya que no te permite exponer el puerto.
#CMD gunicorn todo.wsgi:application --bind 0.0.0.0:$PORT