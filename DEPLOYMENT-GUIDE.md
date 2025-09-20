# Guía de Deployment y CI/CD

## 📋 Resumen Completo del Proyecto

Este proyecto Flask incluye:

### ✅ **Testing Completo** (100% Cobertura)
- **43 tests** implementados
- **100% cobertura** de código (53/53 líneas)
- Testing de modelos, rutas, configuración y aplicación
- Tests unitarios e integración
- Configuración con pytest, pytest-cov y pytest-flask

### ✅ **Docker Environment**
- Multi-container setup con Docker Compose
- PostgreSQL database con persistencia
- Flask app con hot reload
- Jenkins para deployment local
- Configuración automática y scripts de utilidad

### ✅ **CI/CD Pipeline**
- **GitHub Actions**: Validación automática en Pull Requests
- **Jenkins**: Deployment local automatizado
- **Linting**: flake8, black, isort
- **Testing automático**: pytest con coverage reports

## 🚀 Quick Start

### 1. Levantar el proyecto completo
```bash
# Aplicación + Base de datos
docker-compose up --build web db

# Con Jenkins incluido
docker-compose up --build web db jenkins
```

### 2. Ejecutar tests
```bash
./docker.sh test         # Tests con cobertura
./docker.sh test-simple  # Tests sin cobertura
```

### 3. Acceso a servicios
- **Aplicación**: http://localhost:3001
- **Jenkins**: http://localhost:8080
- **Database**: localhost:5432 (postgres:postgres/mydatabase)

## 🔧 Scripts Disponibles

```bash
./docker.sh up           # Levantar todos los servicios
./docker.sh down         # Parar servicios
./docker.sh db           # Solo base de datos
./docker.sh logs         # Ver logs
./docker.sh clean        # Limpiar containers y volumes
./docker.sh test         # Tests con cobertura
./docker.sh test-simple  # Tests básicos
./docker.sh test-file <archivo>  # Test específico
```

## 📊 Testing Coverage Report

```
Name              Stmts   Miss  Cover   Missing
-----------------------------------------------
app/__init__.py      11      0   100%
app/config.py        10      0   100%
app/models.py         6      0   100%
app/routes.py        26      0   100%
-----------------------------------------------
TOTAL                53      0   100%
```

### Test Distribution:
- **Config tests**: 14 tests (configuración, app factory, herencia)
- **Model tests**: 11 tests (CRUD, validaciones, queries)
- **Route tests**: 16 tests (API endpoints, errores, integración)
- **Run tests**: 2 tests (variables de entorno, fallbacks)

## 🔄 CI/CD Workflow

### GitHub Actions (`.github/workflows/ci.yml`)
Se ejecuta automáticamente en **Pull Requests**:

1. **Setup**: Python 3.11, dependencias
2. **Linting**: flake8, black, isort
3. **Testing**: pytest con coverage report
4. **Validación**: coverage mínimo 80%

### Jenkins Pipeline (`Jenkinsfile`)
Para deployment local:

1. **Checkout**: Código desde repositorio
2. **Build & Deploy**: Docker Compose up
3. **Health Check**: Verificación de endpoints
4. **Integration Tests**: Tests en environment real

### Configuración Jenkins Local

1. **Iniciar Jenkins**:
```bash
docker-compose up -d jenkins
```

2. **Setup inicial**:
```bash
# Obtener password inicial
docker exec reto_final_python-jenkins-1 cat /var/jenkins_home/secrets/initialAdminPassword
```

3. **Acceso**: http://localhost:8080

4. **Crear Pipeline Job** con el `Jenkinsfile` incluido

## 📁 Estructura del Proyecto

```
reto_final_python/
├── app/                    # Código de aplicación
│   ├── __init__.py        # App factory
│   ├── config.py          # Configuraciones
│   ├── models.py          # Modelos SQLAlchemy
│   └── routes.py          # API endpoints
├── tests/                  # Suite de tests
│   ├── conftest.py        # Configuración pytest
│   ├── test_models.py     # Tests de modelos
│   ├── test_routes.py     # Tests de API
│   ├── test_config.py     # Tests de configuración
│   └── test_run.py        # Tests de aplicación
├── .github/workflows/      # GitHub Actions
│   └── ci.yml             # Pipeline CI/CD
├── jenkins-docker/         # Jenkins setup
│   └── Dockerfile         # Jenkins con plugins
├── docker-compose.yml      # Orquestación containers
├── Dockerfile             # Flask app image
├── docker-entrypoint.sh   # Script inicialización
├── docker.sh              # Scripts utilidad
├── Jenkinsfile            # Pipeline Jenkins
├── requirements.txt       # Dependencias Python
├── pytest.ini            # Configuración pytest
├── .flake8               # Configuración linting
├── pyproject.toml        # Configuración black/isort
└── README-Docker.md       # Documentación Docker
```

## 🛠️ Configuración de Linting

### flake8 (`.flake8`)
- Max line length: 88
- Exclude: venv, migrations, __pycache__
- Ignore: E203, W503

### black (`pyproject.toml`)
- Line length: 88
- Target version: Python 3.11

### isort (`pyproject.toml`)
- Profile: black
- Multi-line: 3
- Line length: 88

## 🗂️ Base de Datos

### PostgreSQL Configuration
- **Host**: db (container) / localhost (host)
- **Port**: 5432
- **User**: myuser
- **Password**: mypassword
- **Database**: mydatabase

### Modelo de Datos
```python
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
```

## 📋 API Endpoints

- `GET /data` - Obtener todos los datos
- `POST /data` - Crear nuevo dato (JSON: `{"name": "value"}`)
- `DELETE /data/<id>` - Eliminar dato por ID

## 🎯 Casos de Uso Cubiertos

### Desarrollo Local
1. Hot reload habilitado
2. Debug mode activo
3. Tests rápidos con `./docker.sh test`

### Integración Continua
1. Validación automática en PRs
2. Tests y linting obligatorios
3. Coverage report generado

### Deployment
1. Jenkins pipeline automatizado
2. Health checks incluidos
3. Rollback automático en fallas

## ⚡ Performance y Optimización

- **Container caching**: Dockerfile optimizado por capas
- **Test isolation**: Cada test usa transacciones rollback
- **Database persistence**: Volúmenes para PostgreSQL
- **Resource limits**: Configurados en docker-compose

## 🔍 Troubleshooting

### App no responde
```bash
docker-compose logs web
docker-compose ps
```

### Tests fallan
```bash
./docker.sh test-file <nombre_test>
docker exec -it reto_final_python-web-1 bash
```

### Jenkins issues
```bash
docker-compose logs jenkins
docker exec -it reto_final_python-jenkins-1 bash
```

### Database connection
```bash
docker-compose logs db
docker exec -it reto_final_python-db-1 psql -U myuser mydatabase
```

## 🎉 Resultado Final

✅ **80%+ Code Coverage**: 100% logrado  
✅ **PostgreSQL Docker**: Implementado  
✅ **Test Commands**: Scripts automatizados  
✅ **CI/CD Pipeline**: GitHub Actions + Jenkins  
✅ **Production Ready**: Linting, testing, deployment  

¡El proyecto está listo para producción con testing robusto y deployment automatizado!