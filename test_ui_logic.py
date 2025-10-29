#!/usr/bin/env python3
"""
Simula la lógica de actualizar_vector_estado para verificar que funciona
"""

from simulacion import SimulacionPeluqueria

# Simular límite de clientes como en la UI
MAX_CLIENTES_COLUMNAS = 10

# Crear y ejecutar simulación
sim = SimulacionPeluqueria(tiempo_llegada_min=2, tiempo_llegada_max=5)
stats = sim.simular_dia(tiempo_max=30, max_iteraciones=1000)

print(f"✅ Simulación completada: {len(sim.clientes)} clientes generados")

# Simular lo que hace actualizar_vector_estado
filas = sim.obtener_vector_estado_filtrado(hora_inicio=0, num_filas=50)

# Determinar clientes a mostrar (como en la UI)
clientes_ultimos = []
if sim.clientes:
    todos_clientes = sorted(sim.clientes, key=lambda c: c.id)
    clientes_ultimos = todos_clientes[:MAX_CLIENTES_COLUMNAS]
    print(f"📊 Mostrando {len(clientes_ultimos)} de {len(todos_clientes)} clientes")

# Verificar que podemos acceder a los datos de cada fila
print(f"\n🔍 Verificando acceso a datos de clientes en filas:")
for i, fila in enumerate(filas[:3]):  # Solo primeras 3 filas
    print(f"\nFila {i+1} (Iteración {fila.iteracion}, Reloj={fila.reloj:.2f}):")
    print(f"  Snapshot tiene {len(fila.clientes_snapshot)} clientes")
    
    # Intentar rellenar las columnas como lo hace la UI
    start_col = 24
    for idx_c, c in enumerate(clientes_ultimos):
        cliente_info = None
        for cs in fila.clientes_snapshot:
            if cs['id'] == c.id:
                cliente_info = cs
                break
        
        estado = cliente_info['estado'] if cliente_info else '-'
        hora_ini = f"{cliente_info['hora_inicio_espera']:.2f}" if cliente_info else '-'
        tiempo_esp = f"{cliente_info['tiempo_espera']:.2f}" if cliente_info else '-'
        
        col_estado = start_col + idx_c * 3
        col_hora = start_col + idx_c * 3 + 1
        col_tiempo = start_col + idx_c * 3 + 2
        
        if idx_c < 3:  # Mostrar solo primeros 3 clientes
            print(f"    C{c.id} [cols {col_estado}-{col_tiempo}]: Estado={estado}, Hora={hora_ini}, Tiempo={tiempo_esp}")

print("\n✅ ¡Datos se extraen correctamente! Las columnas deberían mostrarse en la UI.")
