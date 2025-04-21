# DevOps Technical Exercise - Django + Kubernetes + CI/CD | DevSu

Este proyecto demuestra la implementación completa del ciclo de vida DevOps para una aplicación Django RESTful, desde el desarrollo local hasta el despliegue automatizado en un clúster Kubernetes con integración continua, entrega continua y mejores prácticas de seguridad y monitoreo.

---

## Descripción General

La aplicación consiste en un sistema básico de gestión de usuarios con Django REST Framework. Permite operaciones CRUD y garantiza unicidad por documento (DNI). Todo el proceso fue diseñado para cumplir los siguientes requerimientos técnicos:

- Dockerización completa de la aplicación.
- Pipeline de CI/CD con pruebas, análisis estático, build y push de imagen.
- Despliegue automatizado en Kubernetes local (Minikube)
- Uso de recursos Kubernetes.

Los mismos fueron divididos en "Fases" que fue la forma en como dividi los pasos a seguir, que tambien iran incluidas como "fases.txt".

---

## Endpoints Disponibles

- `GET /api/users/`  
- `POST /api/users/`  
- `GET /api/users/<id>/`  

---

## Ejecución Local

**1. Requisitos**

- Python 3.11.3  
- pip + virtualenv  
- Docker  
- Git  
- Minikube (con Hyper-V o Docker)  
- kubectl

**2. Clonar el repositorio y preparar entorno**

```bash
git clone https://github.com/AnthonyGrullonA/DevSuPT.git
cd DevSuPT
python -m venv env
source env/bin/activate  # En Windows: env\Scripts\activate
pip install -r requirements.txt
```

**3. Migrar base de datos y levantar servidor local**

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

Visitar: http://localhost:8000/api/users/

---

## Dockerización

En la Fase 2 del proyecto se dockerizó exitosamente la aplicación Django `devsu-demo-devops-python`, permitiendo su ejecución local. Se implementó un Dockerfile con buenas prácticas (imagen `python:3.11-slim`, usuario no root, variables de entorno, `gunicorn`, `healthcheck` y exposición en el puerto 8000), junto a un `entrypoint.sh` que automatiza migraciones y la recolección de archivos estáticos.

El entorno se configuró con `.env` y adaptaciones en `settings.py` poder servir los archivos estaticos de forma correcta. El resultado final fue una aplicación funcional, con migraciones y archivos estáticos gestionados correctamente, lista para ser integrada en flujos de despliegue automatizados.

---

## CI/CD con GitHub Actions

El pipeline realiza:

- Code Checkout  
- Setup de Python 3.11  
- Instalación de dependencias  
- Migraciones Django  
- Ejecución de pruebas unitarias  
- Cobertura con `coverage`  
- Análisis estático con `pylint`  
- Build y Push de la imagen Docker  
- Escaneo de vulnerabilidades con Trivy

Adicionalmente:

- Se levanta un clúster `kind` simulado.
- Se aplican los manifiestos Kubernetes (`kubectl apply -f k8s/`).

![](https://raw.githubusercontent.com/AnthonyGrullonA/img_resources/refs/heads/main/1.png)

![](https://raw.githubusercontent.com/AnthonyGrullonA/img_resources/refs/heads/main/6.png)
---

## Despliegue en Kubernetes

**Recursos utilizados (ubicados en `/k8s`):**

- `deployment.yaml`: define 2 réplicas, expone puerto 8000, y readiness/liveness probes.
- `service.yaml`: tipo ClusterIP expone el contenedor internamente.
- `configmap.yaml`: variables como `ALLOWED_HOSTS`.
- `secrets.yaml`: credenciales sensibles (`SECRET_KEY`, `DATABASE_NAME`).
- `hpa.yaml`: autoescalado basado en CPU.
- `pv.yaml` y `pvc.yaml`: persistencia para `db.sqlite3`.
- `ingress.yaml`: expone la aplicación con host `demopt.local`.

![](https://raw.githubusercontent.com/AnthonyGrullonA/img_resources/refs/heads/main/3.png)

**Despliegue local con Minikube:**

```bash
kubectl apply -f k8s/
minikube addons enable ingress
```

**Validar estado:**

```bash
kubectl get pods
kubectl get svc
kubectl get ingress
```

![](https://raw.githubusercontent.com/AnthonyGrullonA/img_resources/refs/heads/main/4.png)


---

## Acceso a la Aplicación

Una vez desplegado:

1. Asegurar que Minikube está ejecutándose y el addon `ingress` está activado.
2. Añadir a tu archivo `hosts`:

```
ipcluster    demopt.local
```

> Reemplazar con la IP real: `minikube ip`

3. Visitar en navegador:  
http://demopt.local/api/users/

![](https://raw.githubusercontent.com/AnthonyGrullonA/img_resources/refs/heads/main/5.png)


---

## Diagramas

**1. Diagrama de arquitectura**  
![](https://raw.githubusercontent.com/AnthonyGrullonA/img_resources/refs/heads/main/7.png)

**2. Flujo de CI/CD - GitHub Actions**  
![](https://raw.githubusercontent.com/AnthonyGrullonA/img_resources/refs/heads/main/2.png)

---

## Destacados

- SQLite fue utilizada por simplicidad para esta prueba.
- Se diseñó la solución modularmente para soportar orquestadores cloud (AKS, GKE, EKS).
- Las pruebas unitarias abarcan GET, POST, PATCH, DELETE de usuarios.

---

## Estado del Proyecto (Fases detalladas en el archivo de notas)

- [x] Fase 1 - Preparación del entorno  
- [x] Fase 2 - Dockerización  
- [x] Fase 3 - CI/CD Pipeline  
- [x] Fase 4 - Kubernetes Deployment  
- [x] Fase 5 - Integración en Pipeline  
- [x] Fase 6 - Documentación y Diagramas

---


