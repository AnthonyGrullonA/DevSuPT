#!/bin/bash
set -e

echo "→ Aplicando migraciones..."
python manage.py migrate --noinput

echo "→ Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo "→ Iniciando aplicación con gunicorn..."
exec gunicorn demo.wsgi:application --bind 0.0.0.0:8000
