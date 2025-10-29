#!/usr/bin/env python3
"""
Demostración rápida de las columnas de clientes en el Vector de Estado
Ejecuta una simulación corta y muestra las columnas generadas
"""

from simulacion import SimulacionPeluqueria

def demo_columnas_clientes():
    """Demostración de columnas de clientes"""
    
    print("\n" + "🎬 "*30)
    print(" "*20 + "DEMOSTRACIÓN DE COLUMNAS DE CLIENTES")
    print("🎬 "*30 + "\n")
    
    # Crear simulación con parámetros que generen actividad rápida
    print("⚙️  Configurando simulación...")
    sim = SimulacionPeluqueria(
        tiempo_llegada_min=2,
        tiempo_llegada_max=5,
        tiempo_min_aprendiz=8,
        tiempo_max_aprendiz=12,
        tiempo_min_vet_a=6,
        tiempo_max_vet_a=10,
        tiempo_min_vet_b=7,
        tiempo_max_vet_b=11
    )
    
    # Simular 60 minutos
    print("🔄 Ejecutando simulación de 60 minutos...\n")
    stats = sim.simular_dia(tiempo_max=60, max_iteraciones=1000)
    
    print("✅ Simulación completada:")
    print(f"   📊 Total de clientes: {len(sim.clientes)}")
    print(f"   ✂️  Clientes atendidos: {stats['clientes_atendidos']}")
    print(f"   🔢 Iteraciones: {stats['iteraciones']}")
    print(f"   💰 Recaudación: ${stats['recaudacion']:,.0f}")
    
    # Mostrar estructura del vector de estado
    print("\n" + "="*80)
    print("ESTRUCTURA DEL VECTOR DE ESTADO CON COLUMNAS DE CLIENTES")
    print("="*80)
    
    # Mostrar encabezados
    print("\nCOLUMNAS BASE (siempre presentes):")
    columnas_base = [
        "Iter", "Reloj", "Evento", "RND Llegada", "RND Asig", "RND Servicio",
        "Prox. Llegada", "Prox. Fin Apr", "Prox. Fin VetA", "Prox. Fin VetB",
        "Estado Aprendiz", "Cliente Aprendiz", "Cola Aprendiz",
        "Estado Vet A", "Cliente Vet A", "Cola Vet A",
        "Estado Vet B", "Cliente Vet B", "Cola Vet B",
        "Clientes Atend.", "Recaud. Acum", "Costo Refrig", "Refrig. Entregados", "Max Cola"
    ]
    print(f"   Total: {len(columnas_base)} columnas")
    for i, col in enumerate(columnas_base[:5], 1):
        print(f"   {i}. {col}")
    print(f"   ... (y {len(columnas_base)-5} columnas más)")
    
    # Mostrar columnas de clientes (máximo 10 según límite)
    max_clientes_mostrar = min(10, len(sim.clientes))
    print(f"\nCOLUMNAS DE CLIENTES (máximo 10 clientes):")
    print(f"   Clientes a mostrar: {max_clientes_mostrar} de {len(sim.clientes)} totales")
    
    for i in range(min(3, max_clientes_mostrar)):
        base = len(columnas_base) + i * 3
        print(f"   Cliente C{i+1}:")
        print(f"      Col {base+1}: C{i+1} Estado")
        print(f"      Col {base+2}: C{i+1} Hora Inicio")
        print(f"      Col {base+3}: C{i+1} Tiempo Esp")
    
    if max_clientes_mostrar > 3:
        print(f"   ... (y {max_clientes_mostrar - 3} clientes más)")
    
    total_columnas = len(columnas_base) + max_clientes_mostrar * 3
    print(f"\n   📊 TOTAL DE COLUMNAS: {total_columnas}")
    
    # Mostrar algunas filas de ejemplo
    print("\n" + "="*80)
    print("EJEMPLO DE DATOS EN EL VECTOR DE ESTADO")
    print("="*80)
    
    # Tomar algunas filas de ejemplo
    filas_ejemplo = [0, len(sim.vector_estado)//2, -1] if len(sim.vector_estado) > 2 else [0, -1]
    
    for idx in filas_ejemplo:
        fila = sim.vector_estado[idx]
        es_ultima = idx == -1
        
        print(f"\n{'='*80}")
        print(f"FILA {'ÚLTIMA' if es_ultima else idx+1} (Iteración {fila.iteracion}, Reloj={fila.reloj:.2f} min)")
        print(f"{'='*80}")
        
        print(f"Evento: {fila.evento}")
        print(f"Estados peluqueros: Apr={fila.estado_aprendiz}, VetA={fila.estado_veterano_a}, VetB={fila.estado_veterano_b}")
        print(f"Acumuladores: Atendidos={fila.clientes_atendidos}, Recaud=${fila.recaudacion_acum:,.0f}")
        
        print(f"\nClientes en snapshot: {len(fila.clientes_snapshot)}")
        
        if fila.clientes_snapshot:
            print("\nPRIMEROS CLIENTES:")
            print(f"{'ID':<6} {'Estado':<12} {'Hora Inicio':>12} {'Tiempo Esp':>12}")
            print("-"*50)
            
            for cliente in fila.clientes_snapshot[:5]:
                print(f"C{cliente['id']:<5} {cliente['estado']:<12} "
                      f"{cliente['hora_inicio_espera']:>12.2f} "
                      f"{cliente['tiempo_espera']:>12.2f}")
            
            if len(fila.clientes_snapshot) > 5:
                print(f"... y {len(fila.clientes_snapshot) - 5} clientes más")
    
    # Resumen final
    print("\n" + "="*80)
    print("RESUMEN")
    print("="*80)
    print(f"✅ Vector de estado generado con {len(sim.vector_estado)} filas")
    print(f"✅ Cada fila contiene información de {len(sim.clientes)} clientes")
    print(f"✅ En la UI/Excel se mostrarán los primeros {max_clientes_mostrar} clientes como columnas")
    print(f"✅ Cada cliente tiene 3 columnas: Estado, Hora Inicio, Tiempo Espera")
    
    print("\n💡 TIPS:")
    print("   - Para ver más clientes: modificar MAX_CLIENTES_COLUMNAS en main.py")
    print("   - Para exportar: usar el botón '📊 Exportar a Excel' en la UI")
    print("   - Para ver en la UI: ejecutar 'python3 main.py' y simular")
    
    print("\n" + "🎉 "*30)
    print(" "*20 + "¡DEMOSTRACIÓN COMPLETADA!")
    print("🎉 "*30 + "\n")

if __name__ == '__main__':
    demo_columnas_clientes()
