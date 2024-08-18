FROM python:3.12

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD [ "bash", "-c", "while !</dev/tcp/postgres-db/5432; do sleep 1; done; python3 manage.py migrate && gunicorn config.wsgi:application --bind 0.0.0.0:8000" ]
