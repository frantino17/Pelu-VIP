#!/bin/bash

# Script simple para ejecutar la Simulación de Peluquería VIP
# Este script asume que las dependencias ya están instaladas

# Obtener el directorio donde está el script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Ejecutar la aplicación
python3 main.py
