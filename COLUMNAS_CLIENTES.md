# Peluquería VIP - Columnas de Clientes

## Cambios Implementados

### Resumen
Se han añadido columnas dinámicas al **Vector de Estado** para mostrar información detallada de cada cliente (objetos temporales) que pasa por la peluquería.

### Columnas Añadidas por Cliente
Para cada cliente (C1, C2, C3, ...) se muestran tres columnas adicionales:

1. **Estado Cliente**: Indica el estado actual del cliente
   - `Pendiente`: Cliente generado pero aún no ha llegado
   - `Esperando`: Cliente en cola de espera
   - `En Servicio`: Cliente siendo atendido
   - `Atendido`: Cliente que ya terminó su atención

2. **Hora Inicio Espera**: Tiempo de llegada del cliente (en minutos desde el inicio de la jornada)

3. **Tiempo Total Espera**: Tiempo que el cliente esperó antes de ser atendido (en minutos)

### Límite de Columnas
Para evitar tablas enormes, se muestra un **máximo de 10 clientes** como columnas adicionales. Si hay más clientes:
- En la interfaz gráfica: Se muestra un mensaje informativo en la consola
- En el archivo Excel: Se exportan solo los primeros 10 clientes
- Este límite puede ajustarse modificando la constante `MAX_CLIENTES_COLUMNAS` en `main.py`

## Archivos Modificados

### 1. `simulacion.py`
- **Cambio principal**: Añadido campo `clientes_snapshot` a la clase `FilaVectorEstado`
- **Función modificada**: `_registrar_vector_estado()` ahora captura un snapshot de todos los clientes en cada iteración
- **Compatibilidad**: Añadidos parámetros opcionales al constructor para mantener compatibilidad con tests existentes

### 2. `main.py`
- **UI**: La tabla del Vector de Estado ahora genera columnas dinámicamente según los clientes presentes
- **Exportación Excel**: Los archivos Excel incluyen las columnas de clientes con formato apropiado
- **Constante añadida**: `MAX_CLIENTES_COLUMNAS = 10` (límite de clientes mostrados)
- **Mejora**: Uso de `openpyxl.utils.get_column_letter` para manejar correctamente columnas más allá de Z

## Pruebas

### Tests Disponibles

1. **test_validaciones.py** ✅
   - Verifica validación de rangos min/max
   - Verifica validación de probabilidades
   - Estado: PASA

2. **test_parametros.py** ⚠️
   - Verifica que los parámetros sean configurables
   - Verifica inicialización de la UI
   - Estado: Test 1 PASA, Test 2 falla (controles UI faltantes pre-existentes, no relacionados con este cambio)

3. **test_columnas_clientes.py** ✅ (NUEVO)
   - Verifica que las columnas de clientes se generen correctamente
   - Verifica el snapshot de clientes en el vector de estado
   - Estado: PASA

### Ejecutar Tests
```bash
# Test de validaciones
python3 test_validaciones.py

# Test de parámetros
python3 test_parametros.py

# Test de columnas de clientes (nuevo)
python3 test_columnas_clientes.py
```

## Uso

### Interfaz Gráfica
1. Ejecutar la aplicación:
   ```bash
   python3 main.py
   ```

2. Configurar parámetros de simulación en el panel superior

3. Presionar "▶️ Ejecutar Simulación"

4. En la pestaña "📋 Vector de Estado":
   - Ajustar "Hora inicio" y "Número de filas" según necesidad
   - Presionar "🔄 Actualizar Vector"
   - Las columnas de clientes (C1, C2, ...) aparecerán al final de la tabla

5. Para exportar a Excel:
   - Presionar "📊 Exportar a Excel"
   - El archivo incluirá las columnas de clientes en la hoja "Vector de Estado"

### Programático
```python
from simulacion import SimulacionPeluqueria

# Crear simulación
sim = SimulacionPeluqueria()

# Ejecutar simulación
stats = sim.simular_dia()

# Acceder al vector de estado con clientes
for fila in sim.vector_estado:
    print(f"Iteración {fila.iteracion}:")
    for cliente in fila.clientes_snapshot:
        print(f"  C{cliente['id']}: {cliente['estado']} - "
              f"Espera: {cliente['tiempo_espera']:.2f} min")
```

## Estructura de Datos

### FilaVectorEstado.clientes_snapshot
Lista de diccionarios, uno por cada cliente. Cada diccionario contiene:

```python
{
    'id': int,                      # ID único del cliente
    'estado': str,                  # 'Pendiente', 'Esperando', 'En Servicio', 'Atendido'
    'hora_inicio_espera': float,    # Tiempo de llegada (min)
    'tiempo_espera': float          # Tiempo que esperó antes de ser atendido (min)
}
```

## Notas Técnicas

### Rendimiento
- El snapshot se crea en cada iteración de la simulación
- Con el límite de 10 clientes por columna, el impacto es mínimo
- Para simulaciones con cientos de clientes, el snapshot completo se mantiene pero solo se visualizan los primeros 10

### Compatibilidad
- **Backward compatible**: Los parámetros opcionales mantienen compatibilidad con código existente
- **Excel**: Compatible con todas las versiones que soporten openpyxl
- **Python**: Requiere Python 3.7+

### Configuración

Para cambiar el límite de clientes mostrados, editar en `main.py`:

```python
class PeluqueriaVIPApp(QMainWindow):
    # Cambiar este valor según necesidad
    MAX_CLIENTES_COLUMNAS = 10  # Por defecto: 10 clientes
```

## Ejemplo de Salida

### En la Tabla UI
```
| Iter | Reloj | Evento | ... | C1 Estado | C1 Hora Inicio | C1 Tiempo Esp | C2 Estado | C2 Hora Inicio | C2 Tiempo Esp | ...
|------|-------|--------|-----|-----------|----------------|---------------|-----------|----------------|---------------|-----
|  1   | 2.44  | Llegada|     | Esperando | 2.44          | 0.00          | -         | -              | -             |
|  2   | 2.44  | Fin At.|     | En Servic.| 2.44          | 0.00          | -         | -              | -             |
| ...  | ...   | ...    |     | Atendido  | 2.44          | 0.00          | Esperando | 4.51           | 0.00          |
```

### En Excel
Las mismas columnas se exportan con formato numérico apropiado (2 decimales) y bordes.

## Dependencias

### Requeridas
- PyQt5 (interfaz gráfica)
- Python 3.7+

### Opcionales
- openpyxl (para exportación a Excel)
  ```bash
  pip install openpyxl
  ```

## Solución de Problemas

### "Mostrando X de Y clientes totales"
**Mensaje informativo** que aparece cuando hay más de 10 clientes. Es normal y esperado.
- Para ver todos los clientes: aumentar `MAX_CLIENTES_COLUMNAS` en `main.py`
- Nota: Más columnas = tabla más ancha y archivos Excel más grandes

### Columnas de clientes no aparecen
1. Verificar que se ejecutó una simulación completa
2. Presionar "🔄 Actualizar Vector" después de la simulación
3. Verificar que `self.ultima_simulacion` tenga clientes

### Excel no se exporta
1. Verificar que openpyxl esté instalado: `pip install openpyxl`
2. Verificar permisos de escritura en el directorio destino

## Futuras Mejoras Posibles

1. **Filtros de clientes**: Permitir filtrar qué clientes mostrar (por estado, por ID, etc.)
2. **Vista pivotada**: Opción para mostrar clientes como filas en lugar de columnas
3. **Gráficos**: Visualización gráfica del estado de clientes en el tiempo
4. **Exportación CSV**: Alternativa más ligera que Excel para datasets grandes

---

**Autor**: Sistema de Simulación Peluquería VIP  
**Fecha**: 29 de octubre de 2025  
**Versión**: 1.0
