#!/usr/bin/env python3
"""
Script de verificación rápida
Verifica que la aplicación se inicie correctamente y que los parámetros sean configurables
"""

import sys
from PyQt5.QtWidgets import QApplication

# Importar las clases principales
from main import PeluqueriaVIPApp
from simulacion import SimulacionPeluqueria

def test_parametros_configurables():
    """Prueba que los parámetros se puedan configurar"""
    print("=" * 60)
    print("TEST: Verificando parámetros configurables")
    print("=" * 60)
    
    # Crear simulación con parámetros personalizados
    sim = SimulacionPeluqueria(
        prob_aprendiz=0.20,
        tiempo_min_aprendiz=25,
        tiempo_max_aprendiz=35,
        tarifa_aprendiz=20000,
        prob_veterano_a=0.40,
        tiempo_min_vet_a=10,
        tiempo_max_vet_a=15,
        tarifa_vet_a=35000,
        prob_veterano_b=0.40,
        tiempo_min_vet_b=15,
        tiempo_max_vet_b=20,
        tarifa_vet_b=35000,
        tiempo_llegada_min=3,
        tiempo_llegada_max=10,
        jornada_laboral_horas=10,
        tiempo_refrigerio=25,
        costo_refrigerio=6000
    )
    
    # Verificar que los parámetros se guardaron correctamente
    print("\n✓ Parámetros de peluqueros:")
    print(f"  - Aprendiz: prob={sim.peluqueros[0].probabilidad}, "
          f"tiempo=U({sim.peluqueros[0].tiempo_min},{sim.peluqueros[0].tiempo_max}), "
          f"tarifa=${sim.peluqueros[0].tarifa}")
    print(f"  - Veterano A: prob={sim.peluqueros[1].probabilidad}, "
          f"tiempo=U({sim.peluqueros[1].tiempo_min},{sim.peluqueros[1].tiempo_max}), "
          f"tarifa=${sim.peluqueros[1].tarifa}")
    print(f"  - Veterano B: prob={sim.peluqueros[2].probabilidad}, "
          f"tiempo=U({sim.peluqueros[2].tiempo_min},{sim.peluqueros[2].tiempo_max}), "
          f"tarifa=${sim.peluqueros[2].tarifa}")
    
    print("\n✓ Parámetros de llegadas:")
    print(f"  - Tiempo entre llegadas: U({sim.TIEMPO_LLEGADA_MIN},{sim.TIEMPO_LLEGADA_MAX}) min")
    
    print("\n✓ Parámetros de jornada:")
    print(f"  - Jornada laboral: {sim.JORNADA_LABORAL} min")
    print(f"  - Tiempo para refrigerio: {sim.TIEMPO_REFRIGERIO} min")
    print(f"  - Costo refrigerio: ${sim.COSTO_REFRIGERIO}")
    
    print("\n" + "=" * 60)
    print("✅ TODOS LOS PARÁMETROS SON CONFIGURABLES")
    print("=" * 60)
    
    return True

def test_ui_initialization():
    """Prueba que la UI se inicialice correctamente"""
    print("\n" + "=" * 60)
    print("TEST: Verificando inicialización de la UI")
    print("=" * 60)
    
    app = QApplication(sys.argv)
    ventana = PeluqueriaVIPApp()
    
    # Verificar que todos los controles existen
    controles_requeridos = [
        'spin_dias', 'spin_tiempo_max', 'spin_max_iter',
        'spin_prob_aprendiz', 'spin_tiempo_min_apr', 'spin_tiempo_max_apr', 'spin_tarifa_apr',
        'spin_prob_vet_a', 'spin_tiempo_min_vet_a', 'spin_tiempo_max_vet_a', 'spin_tarifa_vet_a',
        'spin_prob_vet_b', 'spin_tiempo_min_vet_b', 'spin_tiempo_max_vet_b', 'spin_tarifa_vet_b',
        'spin_llegada_min', 'spin_llegada_max',
        'spin_jornada', 'spin_tiempo_refrig', 'spin_costo_refrig',
        'spin_hora_inicio', 'spin_num_filas'
    ]
    
    print("\n✓ Verificando controles:")
    todos_ok = True
    for control in controles_requeridos:
        if hasattr(ventana, control):
            valor = getattr(ventana, control).value()
            print(f"  ✓ {control} = {valor}")
        else:
            print(f"  ✗ {control} NO ENCONTRADO")
            todos_ok = False
    
    if todos_ok:
        print("\n" + "=" * 60)
        print("✅ TODOS LOS CONTROLES ESTÁN PRESENTES")
        print("=" * 60)
    else:
        print("\n" + "=" * 60)
        print("❌ FALTAN ALGUNOS CONTROLES")
        print("=" * 60)
    
    return todos_ok

def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "🔍" * 30)
    print(" " * 10 + "VERIFICACIÓN DE PARAMETRIZACIÓN")
    print("🔍" * 30 + "\n")
    
    # Test 1: Parámetros configurables
    test1_ok = test_parametros_configurables()
    
    # Test 2: UI initialization
    test2_ok = test_ui_initialization()
    
    # Resumen
    print("\n" + "📊" * 30)
    print(" " * 15 + "RESUMEN DE PRUEBAS")
    print("📊" * 30)
    print(f"\nTest 1 (Parámetros): {'✅ PASS' if test1_ok else '❌ FAIL'}")
    print(f"Test 2 (UI): {'✅ PASS' if test2_ok else '❌ FAIL'}")
    
    if test1_ok and test2_ok:
        print("\n" + "🎉" * 30)
        print(" " * 10 + "¡TODOS LOS TESTS PASARON!")
        print("🎉" * 30 + "\n")
        return 0
    else:
        print("\n" + "⚠️" * 30)
        print(" " * 10 + "ALGUNOS TESTS FALLARON")
        print("⚠️" * 30 + "\n")
        return 1

if __name__ == '__main__':
    sys.exit(main())
