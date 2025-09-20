# Testing Documentation

## Resultados de Cobertura

✅ **OBJETIVO CUMPLIDO**: Se alcanzó **100% de cobertura de código**
- Objetivo mínimo requerido: 80%
- Cobertura obtenida: 100%

### Detalles por archivo:
- `app/__init__.py`: 100% (11/11 líneas)
- `app/config.py`: 100% (10/10 líneas)
- `app/models.py`: 100% (6/6 líneas)
- `app/routes.py`: 100% (26/26 líneas)
- **TOTAL**: 100% (53/53 líneas)

## Como ejecutar los tests

### En Docker (Recomendado)
```bash
# Ejecutar tests con cobertura
docker exec -it bootcamp-web-1 python -m pytest --cov=app --cov-report=html --cov-report=term-missing tests/

# Solo ejecutar tests
docker exec -it bootcamp-web-1 python -m pytest tests/

# Tests verbosos
docker exec -it bootcamp-web-1 python -m pytest tests/ -v
```

### Localmente (requiere configuración de DB)
```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar tests
python -m pytest --cov=app --cov-report=html --cov-report=term-missing tests/
```

## Estructura de Tests

### 1. Tests de Modelos (`test_models.py`)
- Creación de objetos Data
- Representación string (__repr__)
- Operaciones de base de datos (CRUD)
- Validaciones de campos
- Consultas y filtros

### 2. Tests de Rutas (`test_routes.py`)
- POST /data - Crear datos
- GET /data - Obtener todos los datos
- DELETE /data/<id> - Eliminar datos
- Validaciones de entrada
- Manejo de errores
- Métodos HTTP no permitidos
- Tests de integración completos

### 3. Tests de Configuración (`test_config.py`)
- Clases de configuración (Development/Production)
- Variables de entorno
- Inicialización de la aplicación
- Registro de blueprints
- Configuración de base de datos

### 4. Tests de Aplicación (`test_run.py`)
- Variables de entorno de Flask
- Configuración por defecto

## Reportes de Cobertura

### Reporte en Terminal
Se muestra automáticamente al ejecutar los tests con `--cov-report=term-missing`

### Reporte HTML
Se genera en el directorio `htmlcov/` del contenedor
```bash
# Copiar reporte HTML del contenedor
docker cp bootcamp-web-1:/app/htmlcov ./htmlcov
```

## Warnings y Consideraciones

### Warnings de SQLAlchemy
Los warnings sobre `Query.get()` son normales - indican que se usa una API legacy pero funcional.

### Configuración de Tests
- Los tests usan SQLite en memoria para aislamiento
- Cada test se ejecuta en un contexto limpio
- Variables de entorno se mockean según sea necesario

## Comandos Útiles

### Ver logs de tests
```bash
docker exec -it bootcamp-web-1 python -m pytest tests/ -s
```

### Ejecutar un test específico
```bash
docker exec -it bootcamp-web-1 python -m pytest tests/test_routes.py::TestDataRoutes::test_insert_data_success -v
```

### Ejecutar tests por categoría
```bash
# Solo tests de modelos
docker exec -it bootcamp-web-1 python -m pytest tests/test_models.py -v

# Solo tests de rutas
docker exec -it bootcamp-web-1 python -m pytest tests/test_routes.py -v
```

## Resumen Final

🎯 **Tests creados**: 43 tests
✅ **Tests pasando**: 43/43 (100%)
🔍 **Cobertura**: 100% (53/53 líneas)
⚠️ **Warnings**: 7 (relacionados con SQLAlchemy legacy API)

La batería de tests cumple y supera el objetivo de 80% de cobertura, garantizando que todas las líneas de código están probadas y el código es robusto ante regresiones.