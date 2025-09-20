# Docker Setup

## Requisitos Previos
- Docker
- Docker Compose

## Como usar

### Levantar el proyecto completo
```bash
docker-compose up --build
```

### Solo levantar la base de datos
```bash
docker-compose up db
```

### Levantar con Jenkins
```bash
docker-compose up --build web db jenkins
```

### Detener todos los servicios
```bash
docker-compose down
```

### Detener y eliminar volúmenes
```bash
docker-compose down -v
```

### Batería de Test con ejecucion de bash docker.sh
```bash
./docker.sh test       # Tests con cobertura
./docker.sh test-simple # Tests sin cobertura
./docker.sh test-file <archivo> # Test específico
```

## Configuración

### Base de Datos PostgreSQL
- Host: localhost (desde tu máquina) o db (desde el contenedor web)
- Puerto: 5432
- Usuario: myuser
- Contraseña: mypassword
- Base de datos: mydatabase

### Aplicación Web
- URL: http://localhost:3001
- Hot Reload: Habilitado (los cambios se reflejan automáticamente)

### Jenkins
- URL: http://localhost:8080
- Volume: jenkins_home (persistente)

## Variables de Entorno

El proyecto usa estas variables:
- `DATABASE_URI`: postgresql://myuser:mypassword@db:5432/mydatabase
- `FLASK_ENV`: development
- `FLASK_DEBUG`: 1

## CI/CD Pipeline

### GitHub Actions
Este proyecto incluye un pipeline de CI/CD que se ejecuta automáticamente en Pull Requests:

- **Linting**: Valida el formato del código con `flake8`, `black` e `isort`
- **Testing**: Ejecuta todos los tests con `pytest` y genera reporte de cobertura
- **Coverage**: Requiere mínimo 80% de cobertura de código

### Jenkins (Deployment Local)
Para el deployment local se incluye Jenkins:

1. **Iniciar Jenkins**:
```bash
docker-compose up -d jenkins
```

2. **Acceder a Jenkins**: http://localhost:8080

3. **Configuración inicial**:
```bash
# Obtener password inicial
docker exec bootcamp-jenkins-1 cat /var/jenkins_home/secrets/initialAdminPassword
```

4. **Crear job con el Jenkinsfile** incluido en el proyecto

### Workflow completo
1. **Desarrollo**: Código local con hot reload
2. **Pull Request**: GitHub Actions valida automáticamente
3. **Merge**: Jenkins despliega localmente
4. **Testing**: Tests de integración en environment real

## Comandos Docker Útiles

Para ver los logs de la aplicación:
```bash
docker-compose logs -f web
```

Para ver los logs de PostgreSQL:
```bash
docker-compose logs -f db
```

Para ver los logs de Jenkins:
```bash
docker-compose logs -f jenkins
```

Para ejecutar comandos dentro del contenedor de la aplicación:
```bash
docker exec -it bootcamp-web-1 bash
```

## Endpoints Disponibles

- GET /data - Obtener todos los datos
- POST /data - Crear nuevo dato
- DELETE /data/<id> - Eliminar dato por ID