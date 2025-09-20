# 🔄 Hot Reload y Desarrollo Local

## Flujo de Desarrollo Correcto

### ✅ **Cómo Funciona el Hot Reload**

El `docker-compose.yml` está configurado con:
```yaml
web:
  volumes:
    - .:/app  # 🔥 Hot reload: cambios locales → contenedor automáticamente
```

**Esto significa:**
- ✅ Modificas archivos **LOCALMENTE** (en tu host)
- ✅ Docker **refleja automáticamente** los cambios en el contenedor
- ✅ Flask **refresca automáticamente** la aplicación (debug=True)
- ❌ **NO necesitas** copiar archivos entre contenedor y host

### 🛠️ **Flujo de Desarrollo**

#### 1. **Desarrollo Normal**
```bash
# Levantar servicios
docker-compose up -d web db

# Editar archivos LOCALMENTE en tu editor favorito
# Los cambios se ven automáticamente en http://localhost:3001
```

#### 2. **Linting y Formato**
```bash
# Verificar formato (sin modificar)
./lint.sh check

# Aplicar formato automáticamente 
./lint.sh fix  # Los cambios se aplican LOCALMENTE gracias al hot reload
```

#### 3. **Testing**
```bash
# Ejecutar tests
./docker.sh test

# Test específico
./docker.sh test-file test_models.py
```

#### 4. **Antes del Commit**
```bash
# 1. Aplicar linting
./lint.sh fix

# 2. Verificar que todo esté OK
./lint.sh check

# 3. Ejecutar tests
./docker.sh test

# 4. Commit
git add .
git commit -m "feat: nuevas funcionalidades"
git push
```

### 🚀 **Ventajas del Hot Reload**

1. **Desarrollo rápido**: Cambios instantáneos sin rebuild
2. **Debugging eficiente**: Logs y errores en tiempo real
3. **Testing continuo**: Tests actualizados automáticamente
4. **Linting automático**: Formato aplicado sin copiar archivos

### ⚠️ **Importante**

- **NO ejecutes** `docker cp` para copiar archivos
- **NO necesitas** rebuild después de cambios de código
- **SÍ necesitas** rebuild solo si cambias `Dockerfile` o `requirements.txt`

### 🎯 **Casos Especiales**

#### Cambios que SÍ requieren rebuild:
```bash
# Solo si cambias dependencias o configuración Docker
docker-compose up --build web
```

#### Cambios que NO requieren rebuild:
- ✅ Código Python (.py)
- ✅ Archivos de test
- ✅ Configuraciones de app
- ✅ Scripts (.sh)
- ✅ Documentación (.md)