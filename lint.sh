#!/bin/bash

# Script para aplicar linting y formato automáticamente
# Usar ANTES de hacer commit para evitar fallos en CI

echo "🔧 Aplicando formato y linting automáticamente..."

case "$1" in
    "check")
        echo "📋 Verificando formato sin modificar archivos..."
        
        echo "🔍 Checking Black formatting..."
        if docker exec -it reto_final_python-web-1 black --check --diff . 2>/dev/null; then
            echo "✅ Black: OK"
        else
            echo "❌ Black: Requiere reformateo"
        fi
        
        echo "🔍 Checking isort imports..."
        if docker exec -it reto_final_python-web-1 isort --check-only --diff . 2>/dev/null; then
            echo "✅ isort: OK"  
        else
            echo "❌ isort: Requiere reordenar imports"
        fi
        
        echo "🔍 Checking flake8..."
        if docker exec -it reto_final_python-web-1 flake8 . 2>/dev/null; then
            echo "✅ flake8: OK"
        else
            echo "❌ flake8: Tiene errores de linting"
        fi
        ;;
        
    "fix")
        echo "🔧 Aplicando correcciones automáticamente..."
        
        echo "🔄 Ejecutando isort..."
        docker exec -it reto_final_python-web-1 isort .
        
        echo "🔄 Ejecutando black..."
        docker exec -it reto_final_python-web-1 black .
        
        echo " Verificando flake8..."
        docker exec -it reto_final_python-web-1 flake8 .
        
        echo "✅ Linting aplicado! Los archivos están listos para commit."
        echo "💡 Los cambios se aplicaron automáticamente gracias al hot reload."
        ;;
        
    *)
        echo "Usage: $0 {check|fix}"
        echo "  check  - Verificar formato sin modificar archivos"
        echo "  fix    - Aplicar correcciones automáticamente"
        echo ""
        echo "Ejemplos:"
        echo "  $0 check  # Ver qué necesita arreglarse"
        echo "  $0 fix    # Arreglar automáticamente"
        echo ""
        echo "💡 Tip: Ejecuta './lint.sh fix' antes de hacer commit"
        ;;
esac