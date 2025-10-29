#!/usr/bin/env python3
"""
Script de prueba para validaciones de parámetros
Verifica que las validaciones funcionen correctamente
"""

import sys
from PyQt5.QtWidgets import QApplication
from main import PeluqueriaVIPApp

def test_validacion_rangos():
    """Prueba las validaciones de rangos min/max"""
    print("=" * 60)
    print("TEST: Validación de rangos min/max")
    print("=" * 60)
    
    app = QApplication(sys.argv)
    ventana = PeluqueriaVIPApp()
    
    # Test 1: Tiempo min > max para Aprendiz (DEBE FALLAR)
    print("\n1. Probando: Aprendiz con tiempo_min (35) > tiempo_max (20)...")
    ventana.spin_tiempo_min_apr.setValue(35)
    ventana.spin_tiempo_max_apr.setValue(20)
    valido, mensaje = ventana._validar_parametros()
    if not valido and "Aprendiz" in mensaje and "mínimo" in mensaje:
        print("   ✅ CORRECTO: Se detectó el error")
    else:
        print("   ❌ ERROR: No se detectó el problema")
    
    # Test 2: Tiempo min < max para Aprendiz (DEBE PASAR)
    print("\n2. Probando: Aprendiz con valores correctos (20, 30)...")
    ventana.spin_tiempo_min_apr.setValue(20)
    ventana.spin_tiempo_max_apr.setValue(30)
    valido, mensaje = ventana._validar_parametros()
    if valido:
        print("   ✅ CORRECTO: Parámetros válidos aceptados")
    else:
        print(f"   ❌ ERROR: Parámetros válidos rechazados: {mensaje}")
    
    # Test 3: Probabilidades que suman más de 100% (DEBE FALLAR)
    print("\n3. Probando: Probabilidades Aprendiz(60) + Vet_A(50) = 110% > 100%...")
    ventana.spin_prob_aprendiz.setValue(60)
    ventana.spin_prob_vet_a.setValue(50)
    valido, mensaje = ventana._validar_parametros()
    if not valido and "Probabilidades" in mensaje:
        print("   ✅ CORRECTO: Se detectó el error de probabilidades")
    else:
        print("   ❌ ERROR: No se detectó el problema de probabilidades")
    
    # Test 4: Probabilidades correctas (DEBE PASAR)
    print("\n4. Probando: Probabilidades correctas Aprendiz(15) + Vet_A(45) = 60%...")
    ventana.spin_prob_aprendiz.setValue(15)
    ventana.spin_prob_vet_a.setValue(45)
    valido, mensaje = ventana._validar_parametros()
    if valido:
        print("   ✅ CORRECTO: Probabilidades válidas aceptadas")
    else:
        print(f"   ❌ ERROR: Probabilidades válidas rechazadas: {mensaje}")
    
    # Test 5: Llegadas con min > max (DEBE FALLAR)
    print("\n5. Probando: Llegadas con tiempo_min (15) > tiempo_max (5)...")
    ventana.spin_llegada_min.setValue(15)
    ventana.spin_llegada_max.setValue(5)
    valido, mensaje = ventana._validar_parametros()
    if not valido and "Llegadas" in mensaje:
        print("   ✅ CORRECTO: Se detectó el error en llegadas")
    else:
        print("   ❌ ERROR: No se detectó el problema en llegadas")
    
    # Test 6: Valores correctos completos (DEBE PASAR)
    print("\n6. Probando: Todos los parámetros correctos...")
    ventana.spin_tiempo_min_apr.setValue(20)
    ventana.spin_tiempo_max_apr.setValue(30)
    ventana.spin_tiempo_min_vet_a.setValue(11)
    ventana.spin_tiempo_max_vet_a.setValue(13)
    ventana.spin_tiempo_min_vet_b.setValue(12)
    ventana.spin_tiempo_max_vet_b.setValue(18)
    ventana.spin_llegada_min.setValue(2)
    ventana.spin_llegada_max.setValue(12)
    ventana.spin_prob_aprendiz.setValue(15)
    ventana.spin_prob_vet_a.setValue(45)
    ventana.spin_dias.setValue(30)
    ventana.spin_tiempo_max.setValue(1000)
    ventana.spin_max_iter.setValue(10000)
    ventana.spin_tiempo_refrig.setValue(30)
    
    valido, mensaje = ventana._validar_parametros()
    if valido:
        print("   ✅ CORRECTO: Todos los parámetros válidos aceptados")
    else:
        print(f"   ❌ ERROR: Parámetros válidos rechazados: {mensaje}")
    
    print("\n" + "=" * 60)
    print("PRUEBAS DE VALIDACIÓN COMPLETADAS")
    print("=" * 60)

def main():
    print("\n" + "🔍" * 30)
    print(" " * 10 + "VERIFICACIÓN DE VALIDACIONES")
    print("🔍" * 30 + "\n")
    
    test_validacion_rangos()
    
    print("\n✅ Script de prueba completado exitosamente\n")
    return 0

if __name__ == '__main__':
    sys.exit(main())
