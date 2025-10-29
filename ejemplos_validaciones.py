#!/usr/bin/env python3
"""
Ejemplo de validaciones implementadas en Peluquería VIP
Este archivo muestra ejemplos de código de las validaciones
"""

# ============================================================================
# EJEMPLO 1: Validación en Tiempo Real
# ============================================================================

def _validar_rango_tiempo(self, tipo):
    """
    Valida que el tiempo mínimo no sea mayor que el tiempo máximo en tiempo real.
    Muestra un mensaje temporal si hay error.
    """
    if tipo == 'aprendiz':
        min_val = self.spin_tiempo_min_apr.value()
        max_val = self.spin_tiempo_max_apr.value()
        nombre = "Aprendiz"
    elif tipo == 'vet_a':
        min_val = self.spin_tiempo_min_vet_a.value()
        max_val = self.spin_tiempo_max_vet_a.value()
        nombre = "Veterano A"
    # ... más tipos
    
    # Validar el rango
    if min_val > max_val:
        # Cambiar estilo para indicar error (FONDO ROJO)
        if tipo == 'aprendiz':
            self.spin_tiempo_min_apr.setStyleSheet("QSpinBox { background-color: #ffcccc; }")
            self.spin_tiempo_max_apr.setStyleSheet("QSpinBox { background-color: #ffcccc; }")
    else:
        # Restaurar estilo normal
        if tipo == 'aprendiz':
            self.spin_tiempo_min_apr.setStyleSheet("")
            self.spin_tiempo_max_apr.setStyleSheet("")


# ============================================================================
# EJEMPLO 2: Validación Completa Pre-Ejecución
# ============================================================================

def _validar_parametros(self):
    """
    Valida todos los parámetros de entrada antes de ejecutar la simulación.
    Retorna (bool, str): (es_valido, mensaje_error)
    """
    errores = []
    
    # Validar tiempos mínimos y máximos para cada tipo de peluquero
    if self.spin_tiempo_min_apr.value() > self.spin_tiempo_max_apr.value():
        errores.append("❌ Aprendiz: El tiempo mínimo no puede ser mayor que el tiempo máximo")
    
    if self.spin_tiempo_min_vet_a.value() > self.spin_tiempo_max_vet_a.value():
        errores.append("❌ Veterano A: El tiempo mínimo no puede ser mayor que el tiempo máximo")
    
    # Validar probabilidades (deben sumar 100%)
    prob_aprendiz = self.spin_prob_aprendiz.value()
    prob_vet_a = self.spin_prob_vet_a.value()
    prob_vet_b = 100 - prob_aprendiz - prob_vet_a
    
    if prob_vet_b < 0:
        errores.append(f"❌ Probabilidades: La suma de Aprendiz ({prob_aprendiz}%) "
                      f"y Veterano A ({prob_vet_a}%) excede el 100%")
    
    # Si hay errores, retornar False con los mensajes
    if errores:
        mensaje = "Se encontraron los siguientes errores:\n\n" + "\n".join(errores)
        return False, mensaje
    
    return True, ""


# ============================================================================
# EJEMPLO 3: Integración en Ejecución de Simulación
# ============================================================================

def ejecutar_simulacion(self):
    """Ejecuta la simulación"""
    # PRIMERO: Validar todos los parámetros
    es_valido, mensaje_error = self._validar_parametros()
    if not es_valido:
        # Mostrar cuadro de diálogo con errores
        QMessageBox.warning(self, "Parámetros Inválidos", mensaje_error)
        return  # NO ejecutar si hay errores
    
    # Si todo es válido, continuar con la simulación
    num_dias = self.spin_dias.value()
    tiempo_max = self.spin_tiempo_max.value()
    # ... resto del código


# ============================================================================
# EJEMPLO 4: Conexión de Validación en Tiempo Real
# ============================================================================

# En el constructor de la clase, al crear los SpinBox:

self.spin_tiempo_min_apr = QSpinBox()
self.spin_tiempo_min_apr.setValue(20)
# Conectar a validación en tiempo real
self.spin_tiempo_min_apr.valueChanged.connect(lambda: self._validar_rango_tiempo('aprendiz'))

self.spin_tiempo_max_apr = QSpinBox()
self.spin_tiempo_max_apr.setValue(30)
# Conectar a validación en tiempo real
self.spin_tiempo_max_apr.valueChanged.connect(lambda: self._validar_rango_tiempo('aprendiz'))


# ============================================================================
# CASOS DE PRUEBA
# ============================================================================

"""
CASO 1: Parámetros Inválidos - Tiempo Aprendiz
Input:
  - tiempo_min_apr = 35
  - tiempo_max_apr = 20

Resultado Esperado:
  - Validación en tiempo real: Campos se ponen ROJOS
  - Al ejecutar: Mensaje "❌ Aprendiz: El tiempo mínimo no puede ser mayor que el tiempo máximo"
  - Simulación NO se ejecuta

---

CASO 2: Parámetros Inválidos - Probabilidades
Input:
  - prob_aprendiz = 60
  - prob_vet_a = 50
  - prob_vet_b = -10 (calculada automáticamente)

Resultado Esperado:
  - Label Veterano B muestra en ROJO: "ERROR: -10%"
  - Al ejecutar: Mensaje "❌ Probabilidades: La suma de Aprendiz (60%) y Veterano A (50%) excede el 100%"
  - Simulación NO se ejecuta

---

CASO 3: Parámetros Válidos
Input:
  - tiempo_min_apr = 20, tiempo_max_apr = 30
  - tiempo_min_vet_a = 11, tiempo_max_vet_a = 13
  - prob_aprendiz = 15, prob_vet_a = 45

Resultado Esperado:
  - Todos los campos normales (sin rojo)
  - Label Veterano B muestra en VERDE: "40%"
  - Al ejecutar: Simulación inicia correctamente
  - NO aparece mensaje de error
"""
