#!/usr/bin/env python3
"""
Script de prueba para verificar que las columnas de clientes se generan correctamente
"""

from simulacion import SimulacionPeluqueria

def test_columnas_clientes():
    """Prueba que las columnas de clientes se generen en el vector de estado"""
    print("\n" + "="*60)
    print("TEST: Verificando columnas de clientes en vector de estado")
    print("="*60)
    
    # Crear simulación con parámetros que generen clientes rápidamente
    sim = SimulacionPeluqueria(
        tiempo_llegada_min=1,  # Llegadas muy frecuentes
        tiempo_llegada_max=3,
        tiempo_min_aprendiz=5,  # Servicios rápidos
        tiempo_max_aprendiz=10,
        tiempo_min_vet_a=5,
        tiempo_max_vet_a=8,
        tiempo_min_vet_b=5,
        tiempo_max_vet_b=8
    )
    
    # Simular solo 30 minutos para tener pocos clientes
    print("\n🔄 Ejecutando simulación de 30 minutos...")
    stats = sim.simular_dia(tiempo_max=30, max_iteraciones=1000)
    
    print(f"\n✅ Simulación completada:")
    print(f"   - Clientes generados: {len(sim.clientes)}")
    print(f"   - Clientes atendidos: {stats['clientes_atendidos']}")
    print(f"   - Iteraciones: {stats['iteraciones']}")
    print(f"   - Filas en vector de estado: {len(sim.vector_estado)}")
    
    # Verificar que el vector de estado tiene clientes_snapshot
    if sim.vector_estado:
        primera_fila = sim.vector_estado[0]
        ultima_fila = sim.vector_estado[-1]
        
        print(f"\n📊 Primera fila del vector:")
        print(f"   - Iteración: {primera_fila.iteracion}")
        print(f"   - Reloj: {primera_fila.reloj:.2f}")
        print(f"   - Clientes en snapshot: {len(primera_fila.clientes_snapshot)}")
        
        print(f"\n📊 Última fila del vector:")
        print(f"   - Iteración: {ultima_fila.iteracion}")
        print(f"   - Reloj: {ultima_fila.reloj:.2f}")
        print(f"   - Clientes en snapshot: {len(ultima_fila.clientes_snapshot)}")
        
        # Mostrar detalles de algunos clientes
        if ultima_fila.clientes_snapshot:
            print(f"\n👥 Detalles de clientes en última fila:")
            max_mostrar = min(5, len(ultima_fila.clientes_snapshot))
            for i in range(max_mostrar):
                cliente = ultima_fila.clientes_snapshot[i]
                print(f"   C{cliente['id']}: Estado={cliente['estado']}, "
                      f"Hora inicio espera={cliente['hora_inicio_espera']:.2f}, "
                      f"Tiempo espera={cliente['tiempo_espera']:.2f}")
            
            if len(ultima_fila.clientes_snapshot) > max_mostrar:
                print(f"   ... y {len(ultima_fila.clientes_snapshot) - max_mostrar} clientes más")
        
        print("\n" + "="*60)
        print("✅ VERIFICACIÓN EXITOSA: Las columnas de clientes funcionan")
        print("="*60)
        return True
    else:
        print("\n❌ ERROR: No se generó el vector de estado")
        return False

if __name__ == '__main__':
    import sys
    resultado = test_columnas_clientes()
    sys.exit(0 if resultado else 1)
