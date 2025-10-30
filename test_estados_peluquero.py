#!/usr/bin/env python3
"""
Test para verificar que los estados de clientes incluyen el peluquero asignado
"""

from simulacion import SimulacionPeluqueria

print("\n" + "="*70)
print("TEST: Verificar estados con peluquero asignado")
print("="*70)

# Crear simulación
sim = SimulacionPeluqueria(
    tiempo_llegada_min=2,
    tiempo_llegada_max=4
)

# Simular 25 minutos
print("\n🔄 Ejecutando simulación de 25 minutos...")
stats = sim.simular_dia(tiempo_max=25, max_iteraciones=1000)

print(f"\n✅ Simulación completada:")
print(f"   - Total clientes generados: {len(sim.clientes)}")
print(f"   - Clientes atendidos: {stats['clientes_atendidos']}")

print(f"\n📊 Estados de clientes por iteración (primeras 10 iteraciones):")
print(f"{'Iter':<6} {'Reloj':<8} {'Cliente':<10} {'Estado':<25} {'Peluquero en Estado'}")
print("-"*90)

estados_encontrados = {
    'Esperando Aprendiz': 0,
    'Esperando Vet A': 0,
    'Esperando Vet B': 0,
    'En Servicio Aprendiz': 0,
    'En Servicio Vet A': 0,
    'En Servicio Vet B': 0
}

for i, fila in enumerate(sim.vector_estado[:10]):
    if fila.clientes_snapshot:
        for cliente in fila.clientes_snapshot:
            estado = cliente['estado']
            
            # Contar estados encontrados
            if estado in estados_encontrados:
                estados_encontrados[estado] += 1
            
            # Extraer nombre del peluquero del estado
            if 'Aprendiz' in estado:
                peluquero = '🎓 Aprendiz'
            elif 'Vet A' in estado:
                peluquero = '👨‍🔧 Vet A'
            elif 'Vet B' in estado:
                peluquero = '👨‍🔧 Vet B'
            else:
                peluquero = '❓ Sin especificar'
            
            print(f"{fila.iteracion:<6} {fila.reloj:<8.2f} C{cliente['id']:<9} {estado:<25} {peluquero}")

print(f"\n🔍 Resumen de estados encontrados:")
print(f"{'Estado':<30} {'Cantidad':<10} {'Estado'}")
print("-"*50)

for estado, cantidad in estados_encontrados.items():
    icono = "✅" if cantidad > 0 else "⚪"
    print(f"{estado:<30} {cantidad:<10} {icono}")

# Verificar que al menos algunos estados incluyen el peluquero
total_con_peluquero = sum(estados_encontrados.values())

print(f"\n🎯 Verificación:")
if total_con_peluquero > 0:
    print(f"   ✅ Se encontraron {total_con_peluquero} estados con peluquero especificado")
    print(f"   ✅ Los estados incluyen correctamente el nombre del peluquero")
else:
    print(f"   ❌ No se encontraron estados con peluquero especificado")

# Verificar detalles de algunos clientes
print(f"\n📋 Detalles de clientes en las últimas 3 iteraciones:")
for fila in sim.vector_estado[-3:]:
    print(f"\n   Iteración {fila.iteracion} (t={fila.reloj:.2f}):")
    if fila.clientes_snapshot:
        for cliente in fila.clientes_snapshot:
            print(f"      C{cliente['id']}: {cliente['estado']:<25} (espera: {cliente['tiempo_espera']:.2f} min)")
    else:
        print(f"      (Sin clientes activos)")

print("\n" + "="*70)
print("✅ TEST COMPLETADO")
print("="*70 + "\n")
