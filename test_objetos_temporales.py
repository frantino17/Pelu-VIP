#!/usr/bin/env python3
"""
Test para verificar que los clientes atendidos NO aparecen en el snapshot
(objetos temporales destruidos)
"""

from simulacion import SimulacionPeluqueria

print("\n" + "="*70)
print("TEST: Verificar que clientes atendidos son destruidos del snapshot")
print("="*70)

# Crear simulación
sim = SimulacionPeluqueria(
    tiempo_llegada_min=2,
    tiempo_llegada_max=4,
    tiempo_min_aprendiz=5,
    tiempo_max_aprendiz=8
)

# Simular 30 minutos
print("\n🔄 Ejecutando simulación de 30 minutos...")
stats = sim.simular_dia(tiempo_max=30, max_iteraciones=1000)

print(f"\n✅ Simulación completada:")
print(f"   - Total clientes generados: {len(sim.clientes)}")
print(f"   - Clientes atendidos: {stats['clientes_atendidos']}")
print(f"   - Clientes pendientes: {len(sim.clientes) - stats['clientes_atendidos']}")

print(f"\n📊 Análisis del snapshot por iteración:")
print(f"{'Iter':<6} {'Reloj':<8} {'Evento':<25} {'Clientes Activos':<18} {'IDs en Snapshot'}")
print("-"*90)

for i, fila in enumerate(sim.vector_estado):
    evento_corto = fila.evento[:24]
    ids_snapshot = [f"C{c['id']}" for c in fila.clientes_snapshot]
    ids_str = ", ".join(ids_snapshot) if ids_snapshot else "Ninguno"
    
    # Mostrar primeras 5, algunas del medio y las últimas 3
    if i < 5 or i >= len(sim.vector_estado) - 3:
        print(f"{fila.iteracion:<6} {fila.reloj:<8.2f} {evento_corto:<25} {len(fila.clientes_snapshot):<18} {ids_str}")
    elif i == 5:
        print("  ...")

# Verificar específicamente cuando un cliente termina
print(f"\n🔍 Verificación de destrucción de objetos:")
clientes_finalizados = [c for c in sim.clientes if c.tiempo_fin_atencion > 0 and c.tiempo_fin_atencion <= sim.tiempo_actual]

if clientes_finalizados:
    print(f"\n   Clientes que terminaron su atención: {len(clientes_finalizados)}")
    for c in clientes_finalizados[:3]:
        print(f"   - C{c.id}: Terminó en t={c.tiempo_fin_atencion:.2f} min")
        
        # Buscar en última fila si aparece
        ultima_fila = sim.vector_estado[-1]
        aparece = any(cs['id'] == c.id for cs in ultima_fila.clientes_snapshot)
        
        if aparece:
            print(f"      ❌ ERROR: Cliente aparece en snapshot final (NO debería)")
        else:
            print(f"      ✅ OK: Cliente NO aparece en snapshot final (destruido)")

print(f"\n🎯 Resumen:")
ultima_fila = sim.vector_estado[-1]
print(f"   - Total clientes generados: {len(sim.clientes)}")
print(f"   - Clientes en snapshot final: {len(ultima_fila.clientes_snapshot)}")
print(f"   - Clientes que deberían estar (esperando o en servicio): "
      f"{len(sim.cola_espera) + sum(1 for p in sim.peluqueros if p.estado.value == 'Ocupado')}")

if len(ultima_fila.clientes_snapshot) == len(sim.cola_espera) + sum(1 for p in sim.peluqueros if p.estado.value == 'Ocupado'):
    print("\n✅ ¡CORRECTO! Solo los objetos temporales activos aparecen en el snapshot")
else:
    print("\n⚠️  Advertencia: Discrepancia en cantidad de clientes activos")

print("\n" + "="*70)
