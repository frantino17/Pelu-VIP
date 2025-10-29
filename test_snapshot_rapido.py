#!/usr/bin/env python3
"""
Prueba rápida para verificar que las columnas de clientes se rellenan correctamente
"""

from simulacion import SimulacionPeluqueria

# Crear simulación
sim = SimulacionPeluqueria(
    tiempo_llegada_min=2,
    tiempo_llegada_max=5
)

# Simular 20 minutos
print("🔄 Ejecutando simulación de 20 minutos...")
stats = sim.simular_dia(tiempo_max=20, max_iteraciones=1000)

print(f"✅ Simulación completada:")
print(f"   - Clientes generados: {len(sim.clientes)}")
print(f"   - Iteraciones: {stats['iteraciones']}")

# Verificar que todas las filas tienen clientes_snapshot
print(f"\n🔍 Verificando clientes_snapshot en cada fila:")
filas_con_snapshot = 0
for i, fila in enumerate(sim.vector_estado):
    if fila.clientes_snapshot:
        filas_con_snapshot += 1
    if i < 3 or i == len(sim.vector_estado) - 1:  # Mostrar primeras 3 y última
        print(f"   Fila {i+1}: {len(fila.clientes_snapshot)} clientes en snapshot")
        if fila.clientes_snapshot:
            print(f"      Ejemplo: C{fila.clientes_snapshot[0]['id']} - Estado: {fila.clientes_snapshot[0]['estado']}")

print(f"\n✅ Resultado: {filas_con_snapshot}/{len(sim.vector_estado)} filas tienen clientes_snapshot")

if filas_con_snapshot == len(sim.vector_estado):
    print("✅ ¡PERFECTO! Todas las filas tienen datos de clientes")
else:
    print(f"⚠️  Advertencia: {len(sim.vector_estado) - filas_con_snapshot} filas no tienen clientes_snapshot")
