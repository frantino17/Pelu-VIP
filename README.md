# 🪒 Peluquería ## ✨ Características Principales

### ⚙️ **Parámetros Configurables vs Valores Fijos**

El sistema distingue entre:

#### 🔴 **Parámetros CONFIGURABLES** (valores en ROJO en la interfaz):
- **Probabilidad de asignación Aprendiz** (default: 15%)
- **Probabilidad de asignación Veterano A** (default: 45%)
- **Tiempos de servicio** (mínimo y máximo) para cada peluquero
- **Tiempo entre llegadas** de clientes
- **Tiempo para refrigerio** (minutos de espera antes de recibir bebida)

#### 🟢 **Valores CALCULADOS** (calculados automáticamente):
- **Probabilidad Veterano B:** Se calcula como `100% - prob_aprendiz - prob_vet_a` (ejemplo: 100% - 15% - 45% = 40%)

#### 🟢 **Valores FIJOS** (valores en VERDE en la interfaz - del enunciado):
- **Tarifas de peluqueros:**
  - Aprendiz: $18,000 (FIJO)
  - Veterano A: $32,500 (FIJO)
  - Veterano B: $32,500 (FIJO)
- **Jornada laboral:** 8 horas / 480 minutos (FIJO)
- **Costo de refrigerio:** $5,500 (FIJO)mulación

Sistema de simulación de eventos discretos para una peluquería con interfaz gráfica desarrollada en PyQt5.

---

## 📋 Descripción

Este proyecto simula el funcionamiento de una peluquería con 3 peluqueros (1 aprendiz y 2 veteranos) que atienden clientes con diferentes tiempos de servicio y tarifas. El sistema permite analizar:

1. **Promedio de recaudación diaria**
2. **Cantidad de sillas necesarias** para evitar que clientes esperen de pie
3. **Probabilidad de entregar 5+ refrigerios** en un día

---

## ✨ Características Principales

### ⚙️ **Parámetros Configurables vs Valores Fijos**

El sistema distingue entre:

#### 🔴 **Parámetros CONFIGURABLES** (valores en ROJO en la interfaz):
- **Probabilidades de asignación** de cada peluquero
- **Tiempos de servicio** (mínimo y máximo) para cada peluquero
- **Tiempo entre llegadas** de clientes
- **Tiempo para refrigerio** (minutos de espera antes de recibir bebida)

#### � **Valores FIJOS** (valores en VERDE en la interfaz - del enunciado):
- **Tarifas de peluqueros:**
  - Aprendiz: $18,000 (FIJO)
  - Veterano A: $32,500 (FIJO)
  - Veterano B: $32,500 (FIJO)
- **Jornada laboral:** 8 horas / 480 minutos (FIJO)
- **Costo de refrigerio:** $5,500 (FIJO)

### 📊 Vector de Estado Completo

- Muestra **i iteraciones** desde la **hora j** (ambos configurables)
- **Última fila siempre visible** (resaltada en amarillo)
- **RNDs mostrados** para cada variable aleatoria
- **Estado de objetos**: peluqueros, clientes, colas
- **Acumuladores**: recaudación, refrigerios, max cola

### 🎯 Funcionalidades Adicionales

- ✅ Simulación de múltiples días (1 a 10,000)
- ✅ Exportación a Excel con formato profesional
- ✅ 4 tabs de visualización:
  - Vector de Estado (detallado)
  - Resultados Agregados (respuestas)
  - Resultados Diarios (desglose)
  - Información del Modelo (documentación)
- ✅ Actualización dinámica de filtros
- ✅ Barra de progreso durante simulación
- ✅ Simulación en thread separado (UI no se bloquea)

---

## 🚀 Instalación

### Requisitos Previos

- Python 3.8 o superior
- PyQt5
- openpyxl (opcional, para exportar a Excel)

### Instalación de Dependencias

```bash
cd "/home/pc/Documentos/Facu/SIM/TP4/Pelu VIP"
pip install -r requirements.txt
```

O instalar manualmente:

```bash
pip install PyQt5 openpyxl
```

---

## 💻 Uso

### Ejecutar la Aplicación

```bash
python3 main.py
```

### Pasos para Realizar una Simulación

1. **Configurar Parámetros del Modelo** (valores en ROJO - configurables):
   - Ajustar probabilidades de cada peluquero
   - Configurar tiempos de servicio (mín/máx)
   - Definir tiempo entre llegadas
   - Ajustar tiempo para refrigerio

2. **Configurar Parámetros de Simulación**:
   - Número de días a simular (default: 30)
   - Tiempo máximo por día (default: 1000 min)
   - Máximo de iteraciones (default: 10,000)

3. **Configurar Filtros del Vector**:
   - Desde hora (j): minuto desde el cual mostrar
   - Mostrar (i) filas: cantidad de iteraciones a visualizar

4. **Ejecutar Simulación**:
   - Presionar "▶️ Ejecutar Simulación"
   - Esperar a que finalice (ver barra de progreso)

5. **Analizar Resultados**:
   - **Vector de Estado**: Ver detalle de iteraciones
   - **Resultados Agregados**: Ver respuestas a las 3 preguntas
   - **Resultados Diarios**: Ver desglose por día
   - **Información**: Ver configuración actual

6. **Exportar** (opcional):
   - Presionar "📊 Exportar a Excel"
   - Guardar archivo con timestamp

---

## 📊 Estructura de Archivos

```
Pelu VIP/
│
├── main.py                      # Interfaz gráfica (PyQt5)
├── simulacion.py                # Motor de simulación
├── requirements.txt             # Dependencias
├── test_parametros.py          # Tests de verificación
│
├── CAMBIOS_PARAMETRIZACION.md  # Documentación de cambios
├── CHECKLIST_VERIFICACION.md   # Checklist de requisitos
├── README.md                    # Este archivo
│
└── simulacion_peluqueria_*.xlsx # Exportaciones (generadas)
```

---

## 🧪 Verificación

Para verificar que todos los parámetros son configurables:

```bash
python3 test_parametros.py
```

Debería mostrar:
```
✅ TODOS LOS PARÁMETROS SON CONFIGURABLES
✅ TODOS LOS CONTROLES ESTÁN PRESENTES
🎉 ¡TODOS LOS TESTS PASARON!
```

---

## 📐 Fórmulas Implementadas

### 1. Recaudación Promedio Diaria
```
Recaudación_Promedio = Σ(Recaudación_i) / N

Donde:
- N = número de días simulados
- Recaudación_i = Σ(Tarifa_peluquero × Clientes_atendidos) del día i
```

### 2. Cantidad de Sillas Necesarias
```
Sillas = MAX(Cola_Total_t) para todo t en todos los días

Donde:
- Cola_Total_t = número de clientes esperando en el tiempo t
```

### 3. Probabilidad de 5+ Refrigerios
```
P(Refrigerios ≥ 5) = Días_con_5_o_más / N

Donde:
- Días_con_5_o_más = cantidad de días con 5+ refrigerios entregados
- N = total de días simulados
```

### 4. Ganancia Neta
```
Ganancia = Recaudación - Costo_Refrigerios

Donde:
- Costo_Refrigerios = N_Refrigerios × Costo_Unitario
```

---

## 🎲 Método de Simulación

Se utiliza **simulación por eventos discretos**:

### Eventos Modelados:
1. **Llegada de Cliente**: Generada con U(tiempo_min, tiempo_max)
2. **Fin de Atención**: Cuando un peluquero termina de atender
3. **Entrega de Refrigerio**: Cuando cliente espera > tiempo_refrigerio

### Variables Aleatorias:
- **Tiempo entre llegadas**: U(2, 12) minutos (configurable)
- **Asignación de peluquero**: Según probabilidades acumuladas
- **Tiempo de servicio**: U(min, max) según tipo de peluquero

### RNDs Registrados:
- RND para llegada
- RND para asignación de peluquero
- RND para tiempo de servicio

---

## 📱 Capturas de Pantalla

### Panel de Configuración
Todos los parámetros son editables desde la interfaz:
- Probabilidades de peluqueros
- Tiempos de servicio (min/max)
- Tarifas
- Llegadas de clientes
- Jornada laboral
- Política de refrigerios

### Vector de Estado
Muestra:
- Iteración, Reloj, Evento
- RNDs utilizados
- Próximos eventos programados
- Estado de cada peluquero
- Colas de espera
- Acumuladores

### Resultados Agregados
Responde las 3 preguntas del enunciado con gráficos y valores numéricos.

---

## 🔧 Solución de Problemas

### Error: "No module named 'PyQt5'"
```bash
pip install PyQt5
```

### Error: "No module named 'openpyxl'"
```bash
pip install openpyxl
```

### La simulación es muy lenta
- Reducir número de días
- Reducir tiempo máximo por día
- Reducir máximo de iteraciones

### No se muestra la última fila en el vector
- Verificar que la simulación haya finalizado
- Presionar "🔄 Actualizar Vector"

---

## 👨‍💻 Desarrollo

### Arquitectura

- **Model (simulacion.py)**: Lógica de simulación, eventos discretos
- **View (main.py)**: Interfaz gráfica con PyQt5
- **Threading**: Simulación en thread separado para no bloquear UI

### Patrones Utilizados

- **MVC**: Separación modelo-vista
- **Observer**: Signals/Slots de PyQt5
- **Strategy**: Diferentes tipos de peluqueros

---

## 📝 Cumplimiento del Enunciado

### ✅ Requisitos Parte B:

- [x] Simular X tiempo (parámetro solicitado)
- [x] Generar hasta 100,000 iteraciones
- [x] Mostrar i iteraciones desde hora j
- [x] Mostrar última fila siempre
- [x] **TODOS los valores en ROJO parametrizables** (18/18)
- [x] Vector muestra: hora, evento, próximos eventos, objetos, RNDs
- [x] Variables auxiliares (acumuladores, contadores)
- [x] Fórmulas planteadas

---

## 📞 Contacto

**Proyecto:** Trabajo Práctico 4 - Simulación
**Materia:** Simulación
**Facultad:** [Tu Facultad]

---

## 📄 Licencia

Este proyecto es de uso académico.

---

## 🎉 ¡Gracias!

Esperamos que esta herramienta sea útil para el análisis de la Peluquería VIP.

**Estado:** ✅ Completado al 100%
**Última actualización:** 29 de octubre de 2025
