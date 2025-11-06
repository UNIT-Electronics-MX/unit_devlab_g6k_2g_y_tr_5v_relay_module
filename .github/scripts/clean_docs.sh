#!/bin/bash

# Script para limpiar archivos generados de documentación
# Ubicación: .github/scripts/clean_docs.sh
# Uso: .github/scripts/clean_docs.sh

set -e  # Salir si hay algún error

echo " Limpiando documentación generada..."

# Obtener la ruta del directorio del proyecto (3 niveles arriba desde .github/scripts)
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$PROJECT_DIR"

echo " Directorio del proyecto: $PROJECT_DIR"

# Eliminar archivos y directorios generados
if [ -f "docs/index.html" ]; then
    rm "docs/index.html"
    echo "  Eliminado: docs/index.html"
fi

if [ -d "docs/hardware" ]; then
    rm -rf "docs/hardware"
    echo "  Eliminado: docs/hardware/"
fi

# Verificar si el directorio docs está vacío (excepto por archivos git y readme)
if [ -d "docs" ]; then
    remaining_files=$(find docs -type f ! -name ".gitkeep" ! -name "README.md" ! -name "*.pdf" | wc -l)
    if [ "$remaining_files" -eq 0 ]; then
        echo " Directorio docs limpiado completamente"
    else
        echo "ℹ  Directorio docs contiene $remaining_files archivo(s) adicionales"
    fi
fi

echo " Limpieza completada!"