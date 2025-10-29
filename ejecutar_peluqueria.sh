#!/bin/bash

# Script para ejecutar la Simulación de Peluquería VIP
# Autor: Sistema de Simulación
# Fecha: 29 de octubre de 2025

# Colores para mensajes
VERDE='\033[0;32m'
ROJO='\033[0;31m'
AMARILLO='\033[1;33m'
NC='\033[0m' # Sin Color

echo "================================================"
echo "   Simulación de Peluquería VIP - Iniciador   "
echo "================================================"
echo ""

# Obtener el directorio donde está el script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Verificar que Python3 está instalado
echo -n "Verificando Python3... "
if ! command -v python3 &> /dev/null; then
    echo -e "${ROJO}ERROR${NC}"
    echo "Python3 no está instalado. Por favor, instálalo primero."
    exit 1
fi
echo -e "${VERDE}OK${NC} ($(python3 --version))"

# Verificar que pip3 está instalado
echo -n "Verificando pip3... "
if ! command -v pip3 &> /dev/null; then
    echo -e "${AMARILLO}ADVERTENCIA${NC}"
    echo "pip3 no está instalado. Intentando instalar dependencias manualmente..."
else
    echo -e "${VERDE}OK${NC}"
fi

# Verificar/Instalar dependencias
echo ""
echo "Verificando dependencias de Python..."

# Intentar importar los módulos necesarios
python3 -c "import PyQt5, openpyxl, numpy" 2>/dev/null
if [ $? -eq 0 ]; then
    echo -e "${VERDE}Todas las dependencias están instaladas${NC}"
else
    echo -e "${AMARILLO}Faltan algunas dependencias${NC}"
    echo "Por favor, instala las dependencias usando uno de estos métodos:"
    echo ""
    echo "Método 1 - Paquetes del sistema (recomendado para Linux Mint):"
    echo "  sudo apt install python3-pyqt5 python3-openpyxl python3-numpy"
    echo ""
    echo "Método 2 - Con pip en entorno virtual:"
    echo "  python3 -m venv venv"
    echo "  source venv/bin/activate"
    echo "  pip install -r requirements.txt"
    echo ""
    read -p "¿Deseas continuar de todas formas? (s/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi

# Verificar que los archivos principales existen
echo ""
echo "Verificando archivos del proyecto..."

if [ ! -f "main.py" ]; then
    echo -e "${ROJO}ERROR: No se encuentra main.py${NC}"
    exit 1
fi

if [ ! -f "simulacion.py" ]; then
    echo -e "${ROJO}ERROR: No se encuentra simulacion.py${NC}"
    exit 1
fi

echo -e "${VERDE}Todos los archivos encontrados${NC}"

# Ejecutar la aplicación
echo ""
echo "================================================"
echo "Iniciando aplicación..."
echo "================================================"
echo ""

python3 main.py

# Capturar código de salida
EXIT_CODE=$?

echo ""
echo "================================================"
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${VERDE}Aplicación cerrada correctamente${NC}"
else
    echo -e "${ROJO}La aplicación terminó con errores (código: $EXIT_CODE)${NC}"
fi
echo "================================================"

exit $EXIT_CODE
