"""
Simulación de Peluquería VIP
Motor de simulación con eventos discretos
"""

import random
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class EstadoPeluquero(Enum):
    LIBRE = "Libre"
    OCUPADO = "Ocupado"


class TipoPeluquero(Enum):
    APRENDIZ = "Aprendiz"
    VETERANO_A = "Veterano A"
    VETERANO_B = "Veterano B"


@dataclass
class Peluquero:
    """Representa un peluquero de la peluquería"""
    tipo: TipoPeluquero
    probabilidad: float
    tiempo_min: int
    tiempo_max: int
    tarifa: int
    estado: EstadoPeluquero = EstadoPeluquero.LIBRE
    cliente_actual: Optional['Cliente'] = None
    tiempo_fin_atencion: float = 0.0
    
    def asignar_cliente(self, cliente: 'Cliente', tiempo_inicio: float):
        """Asigna un cliente al peluquero"""
        self.estado = EstadoPeluquero.OCUPADO
        self.cliente_actual = cliente
        tiempo_servicio = random.uniform(self.tiempo_min, self.tiempo_max)
        self.tiempo_fin_atencion = tiempo_inicio + tiempo_servicio
        return tiempo_servicio
    
    def liberar(self):
        """Libera al peluquero"""
        self.estado = EstadoPeluquero.LIBRE
        self.cliente_actual = None
        self.tiempo_fin_atencion = 0.0


@dataclass
class Cliente:
    """Representa un cliente de la peluquería"""
    id: int
    tiempo_llegada: float
    peluquero_asignado: Optional[Peluquero] = None
    tiempo_inicio_atencion: float = 0.0
    tiempo_fin_atencion: float = 0.0
    recibio_refrigerio: bool = False
    tiempo_refrigerio: float = 0.0
    
    @property
    def tiempo_espera(self) -> float:
        """Calcula el tiempo de espera del cliente"""
        if self.tiempo_inicio_atencion > 0:
            return self.tiempo_inicio_atencion - self.tiempo_llegada
        return 0.0
    
    @property
    def tiempo_total(self) -> float:
        """Calcula el tiempo total del cliente en la peluquería"""
        if self.tiempo_fin_atencion > 0:
            return self.tiempo_fin_atencion - self.tiempo_llegada
        return 0.0


class TipoEvento(Enum):
    LLEGADA_CLIENTE = "Llegada Cliente"
    FIN_ATENCION = "Fin Atención"
    REFRIGERIO = "Refrigerio"


@dataclass
class Evento:
    """Representa un evento en la simulación"""
    tiempo: float
    tipo: TipoEvento
    cliente: Optional[Cliente] = None
    peluquero: Optional[Peluquero] = None
    descripcion: str = ""


@dataclass
class FilaVectorEstado:
    """Representa una fila del vector de estado"""
    iteracion: int
    reloj: float
    evento: str
    rnd_evento: dict  # Diccionario con todos los RND usados
    
    # Próximos eventos
    proximo_llegada: float
    proximo_fin_aprendiz: float
    proximo_fin_veterano_a: float
    proximo_fin_veterano_b: float
    
    # Estado de peluqueros
    estado_aprendiz: str
    estado_veterano_a: str
    estado_veterano_b: str
    
    # Cliente siendo atendido (ID)
    cliente_aprendiz: str
    cliente_veterano_a: str
    cliente_veterano_b: str
    
    # Colas de espera
    cola_aprendiz: int
    cola_veterano_a: int
    cola_veterano_b: int
    
    # Acumuladores
    clientes_atendidos: int
    recaudacion_acum: float
    costo_refrigerios_acum: float
    clientes_con_refrigerio: int
    max_cola_total: int
    
    # Tiempo fin de atención de cada peluquero
    tiempo_fin_aprendiz: float
    tiempo_fin_veterano_a: float
    tiempo_fin_veterano_b: float


class SimulacionPeluqueria:
    """Motor de simulación de la peluquería"""
    
    JORNADA_LABORAL = 8 * 60  # 8 horas en minutos
    TIEMPO_REFRIGERIO = 30  # minutos
    COSTO_REFRIGERIO = 5500
    
    def __init__(self):
        self.peluqueros: List[Peluquero] = []
        self.clientes: List[Cliente] = []
        self.cola_espera: List[Cliente] = []
        self.eventos: List[Evento] = []
        
        self.tiempo_actual = 0.0
        self.cliente_contador = 0
        self.iteracion = 0
        
        # Estadísticas
        self.recaudacion_total = 0.0
        self.costo_refrigerios = 0.0
        self.max_clientes_esperando = 0
        self.clientes_con_refrigerio = 0
        self.clientes_atendidos_total = 0
        
        # Vector de estado
        self.vector_estado: List[FilaVectorEstado] = []
        
        # Próximo evento de llegada
        self.proximo_llegada = 0.0
        
        # RNDs temporales para registro
        self.ultimo_rnd = {}
        
        self._inicializar_peluqueros()
    
    def _inicializar_peluqueros(self):
        """Inicializa los tres peluqueros"""
        self.peluqueros = [
            Peluquero(TipoPeluquero.APRENDIZ, 0.15, 20, 30, 18000),
            Peluquero(TipoPeluquero.VETERANO_A, 0.45, 11, 13, 32500),
            Peluquero(TipoPeluquero.VETERANO_B, 0.40, 12, 18, 32500)
        ]
    
    def reiniciar(self):
        """Reinicia la simulación"""
        self.clientes = []
        self.cola_espera = []
        self.eventos = []
        self.tiempo_actual = 0.0
        self.cliente_contador = 0
        self.iteracion = 0
        self.recaudacion_total = 0.0
        self.costo_refrigerios = 0.0
        self.max_clientes_esperando = 0
        self.clientes_con_refrigerio = 0
        self.clientes_atendidos_total = 0
        self.vector_estado = []
        self.proximo_llegada = 0.0
        self.ultimo_rnd = {}
        
        for peluquero in self.peluqueros:
            peluquero.liberar()
    
    def _seleccionar_peluquero(self) -> Peluquero:
        """Selecciona un peluquero basado en las probabilidades"""
        rand = random.random()
        acumulado = 0.0
        
        for peluquero in self.peluqueros:
            acumulado += peluquero.probabilidad
            if rand <= acumulado:
                return peluquero
        
        return self.peluqueros[-1]
    
    def _generar_llegada_cliente(self):
        """Genera un nuevo cliente"""
        rnd_llegada = random.random()
        tiempo_entre_llegadas = 2 + rnd_llegada * (12 - 2)  # U(2, 12)
        tiempo_llegada = self.tiempo_actual + tiempo_entre_llegadas
        
        self.ultimo_rnd['llegada'] = rnd_llegada
        self.ultimo_rnd['tiempo_entre_llegadas'] = tiempo_entre_llegadas
        
        # Solo generar llegadas durante la jornada laboral
        if tiempo_llegada <= self.JORNADA_LABORAL:
            self.cliente_contador += 1
            cliente = Cliente(id=self.cliente_contador, tiempo_llegada=tiempo_llegada)
            self.clientes.append(cliente)
            
            evento = Evento(
                tiempo=tiempo_llegada,
                tipo=TipoEvento.LLEGADA_CLIENTE,
                cliente=cliente,
                descripcion=f"Cliente {cliente.id} llega"
            )
            self.eventos.append(evento)
            self.proximo_llegada = tiempo_llegada
        else:
            self.proximo_llegada = float('inf')
    
    def _atender_cliente(self, cliente: Cliente):
        """Asigna un cliente a un peluquero"""
        # Seleccionar peluquero según probabilidades
        rnd_peluquero = random.random()
        self.ultimo_rnd['asignacion_peluquero'] = rnd_peluquero
        
        peluquero = self._seleccionar_peluquero_con_rnd(rnd_peluquero)
        cliente.peluquero_asignado = peluquero
        
        # Verificar si hay peluquero del tipo seleccionado disponible
        if peluquero.estado == EstadoPeluquero.LIBRE:
            self._iniciar_atencion(cliente, peluquero)
        else:
            # Agregar a cola de espera
            self.cola_espera.append(cliente)
            cola_total = len(self.cola_espera)
            self.max_clientes_esperando = max(self.max_clientes_esperando, cola_total)
            
            # Programar refrigerio si espera más de 30 minutos
            tiempo_refrigerio = self.tiempo_actual + self.TIEMPO_REFRIGERIO
            evento_refrigerio = Evento(
                tiempo=tiempo_refrigerio,
                tipo=TipoEvento.REFRIGERIO,
                cliente=cliente,
                descripcion=f"Cliente {cliente.id} recibe refrigerio"
            )
            self.eventos.append(evento_refrigerio)
    
    def _seleccionar_peluquero_con_rnd(self, rnd: float) -> Peluquero:
        """Selecciona un peluquero basado en un RND dado"""
        if rnd <= 0.15:
            return self.peluqueros[0]  # Aprendiz
        elif rnd <= 0.60:  # 0.15 + 0.45
            return self.peluqueros[1]  # Veterano A
        else:
            return self.peluqueros[2]  # Veterano B
    
    def _iniciar_atencion(self, cliente: Cliente, peluquero: Peluquero):
        """Inicia la atención de un cliente"""
        cliente.tiempo_inicio_atencion = self.tiempo_actual
        
        # Generar tiempo de servicio con RND
        rnd_servicio = random.random()
        tiempo_servicio = peluquero.tiempo_min + rnd_servicio * (peluquero.tiempo_max - peluquero.tiempo_min)
        self.ultimo_rnd['tiempo_servicio'] = rnd_servicio
        self.ultimo_rnd['duracion_servicio'] = tiempo_servicio
        
        peluquero.asignar_cliente(cliente, self.tiempo_actual)
        peluquero.tiempo_fin_atencion = self.tiempo_actual + tiempo_servicio
        cliente.tiempo_fin_atencion = peluquero.tiempo_fin_atencion
        
        # Programar fin de atención
        evento = Evento(
            tiempo=peluquero.tiempo_fin_atencion,
            tipo=TipoEvento.FIN_ATENCION,
            cliente=cliente,
            peluquero=peluquero,
            descripcion=f"Cliente {cliente.id} termina con {peluquero.tipo.value}"
        )
        self.eventos.append(evento)
        
        # Registrar recaudación
        self.recaudacion_total += peluquero.tarifa
    
    def _procesar_evento(self, evento: Evento):
        """Procesa un evento"""
        self.tiempo_actual = evento.tiempo
        self.iteracion += 1
        self.ultimo_rnd = {}  # Resetear RNDs
        
        nombre_evento = ""
        
        if evento.tipo == TipoEvento.LLEGADA_CLIENTE:
            nombre_evento = f"Llegada Cliente {evento.cliente.id}"
            self._atender_cliente(evento.cliente)
            self._generar_llegada_cliente()
        
        elif evento.tipo == TipoEvento.FIN_ATENCION:
            peluquero = evento.peluquero
            nombre_evento = f"Fin Atención C{evento.cliente.id} ({peluquero.tipo.value})"
            self.clientes_atendidos_total += 1
            peluquero.liberar()
            
            # Atender siguiente cliente en cola del mismo tipo de peluquero
            clientes_en_espera = [c for c in self.cola_espera 
                                 if c.peluquero_asignado == peluquero 
                                 and c.tiempo_inicio_atencion == 0]
            
            if clientes_en_espera:
                siguiente = clientes_en_espera[0]
                self.cola_espera.remove(siguiente)
                self._iniciar_atencion(siguiente, peluquero)
        
        elif evento.tipo == TipoEvento.REFRIGERIO:
            cliente = evento.cliente
            nombre_evento = f"Refrigerio Cliente {cliente.id}"
            # Solo dar refrigerio si aún está esperando
            if cliente.tiempo_inicio_atencion == 0 or cliente.tiempo_inicio_atencion > evento.tiempo:
                if not cliente.recibio_refrigerio:
                    cliente.recibio_refrigerio = True
                    cliente.tiempo_refrigerio = evento.tiempo
                    self.costo_refrigerios += self.COSTO_REFRIGERIO
                    self.clientes_con_refrigerio += 1
        
        # Registrar fila del vector de estado
        self._registrar_vector_estado(nombre_evento)
    
    def _registrar_vector_estado(self, nombre_evento: str):
        """Registra una fila en el vector de estado"""
        aprendiz = self.peluqueros[0]
        veterano_a = self.peluqueros[1]
        veterano_b = self.peluqueros[2]
        
        # Calcular próximos eventos
        proximos_eventos = [e for e in self.eventos if e.tiempo >= self.tiempo_actual]
        
        proximo_llegada = self.proximo_llegada if self.proximo_llegada != float('inf') else 0
        
        # Encontrar próximo fin de atención para cada peluquero
        proximo_fin_aprendiz = 0.0
        proximo_fin_vet_a = 0.0
        proximo_fin_vet_b = 0.0
        
        for evento in proximos_eventos:
            if evento.tipo == TipoEvento.FIN_ATENCION and evento.peluquero:
                if evento.peluquero.tipo == TipoPeluquero.APRENDIZ:
                    proximo_fin_aprendiz = evento.tiempo
                elif evento.peluquero.tipo == TipoPeluquero.VETERANO_A:
                    proximo_fin_vet_a = evento.tiempo
                elif evento.peluquero.tipo == TipoPeluquero.VETERANO_B:
                    proximo_fin_vet_b = evento.tiempo
        
        # Contar clientes en cada cola
        cola_aprendiz = len([c for c in self.cola_espera if c.peluquero_asignado == aprendiz])
        cola_vet_a = len([c for c in self.cola_espera if c.peluquero_asignado == veterano_a])
        cola_vet_b = len([c for c in self.cola_espera if c.peluquero_asignado == veterano_b])
        
        fila = FilaVectorEstado(
            iteracion=self.iteracion,
            reloj=self.tiempo_actual,
            evento=nombre_evento,
            rnd_evento=self.ultimo_rnd.copy(),
            
            # Próximos eventos
            proximo_llegada=proximo_llegada,
            proximo_fin_aprendiz=proximo_fin_aprendiz,
            proximo_fin_veterano_a=proximo_fin_vet_a,
            proximo_fin_veterano_b=proximo_fin_vet_b,
            
            # Estado peluqueros
            estado_aprendiz=aprendiz.estado.value,
            estado_veterano_a=veterano_a.estado.value,
            estado_veterano_b=veterano_b.estado.value,
            
            # Clientes atendiendo
            cliente_aprendiz=f"C{aprendiz.cliente_actual.id}" if aprendiz.cliente_actual else "-",
            cliente_veterano_a=f"C{veterano_a.cliente_actual.id}" if veterano_a.cliente_actual else "-",
            cliente_veterano_b=f"C{veterano_b.cliente_actual.id}" if veterano_b.cliente_actual else "-",
            
            # Colas
            cola_aprendiz=cola_aprendiz,
            cola_veterano_a=cola_vet_a,
            cola_veterano_b=cola_vet_b,
            
            # Acumuladores
            clientes_atendidos=self.clientes_atendidos_total,
            recaudacion_acum=self.recaudacion_total,
            costo_refrigerios_acum=self.costo_refrigerios,
            clientes_con_refrigerio=self.clientes_con_refrigerio,
            max_cola_total=self.max_clientes_esperando,
            
            # Tiempos fin
            tiempo_fin_aprendiz=aprendiz.tiempo_fin_atencion,
            tiempo_fin_veterano_a=veterano_a.tiempo_fin_atencion,
            tiempo_fin_veterano_b=veterano_b.tiempo_fin_atencion
        )
        
        self.vector_estado.append(fila)
    
    def simular_dia(self, tiempo_max=None, max_iteraciones=100000):
        """Simula un día de trabajo
        
        Args:
            tiempo_max: Tiempo máximo de simulación en minutos (por defecto jornada completa)
            max_iteraciones: Máximo número de iteraciones permitidas
        """
        self.reiniciar()
        
        if tiempo_max is None:
            tiempo_max = self.JORNADA_LABORAL * 2  # Permitir tiempo extra para terminar
        
        # Generar primer cliente
        self._generar_llegada_cliente()
        
        # Procesar eventos mientras haya eventos pendientes
        while self.eventos and self.iteracion < max_iteraciones:
            # Ordenar eventos por tiempo
            self.eventos.sort(key=lambda e: e.tiempo)
            
            # Procesar siguiente evento
            evento = self.eventos.pop(0)
            
            # Si el evento supera el tiempo máximo, detener
            if evento.tiempo > tiempo_max:
                break
            
            # Si el evento es después de la jornada y no es fin de atención, ignorar
            if evento.tiempo > self.JORNADA_LABORAL and evento.tipo == TipoEvento.LLEGADA_CLIENTE:
                continue
            
            self._procesar_evento(evento)
            
            # Terminar cuando no queden clientes por atender y todos los peluqueros estén libres
            if (self.tiempo_actual > self.JORNADA_LABORAL and 
                not self.cola_espera and 
                all(p.estado == EstadoPeluquero.LIBRE for p in self.peluqueros)):
                break
        
        return self._obtener_estadisticas_dia()
    
    def _obtener_estadisticas_dia(self):
        """Obtiene las estadísticas del día simulado"""
        return {
            'recaudacion': self.recaudacion_total,
            'costo_refrigerios': self.costo_refrigerios,
            'ganancia_neta': self.recaudacion_total - self.costo_refrigerios,
            'clientes_atendidos': self.clientes_atendidos_total,
            'clientes_con_refrigerio': self.clientes_con_refrigerio,
            'max_sillas_necesarias': self.max_clientes_esperando,
            'tiempo_fin': self.tiempo_actual,
            'iteraciones': self.iteracion
        }
    
    def obtener_vector_estado_filtrado(self, hora_inicio=0, num_filas=None):
        """Obtiene el vector de estado filtrado
        
        Args:
            hora_inicio: Hora desde la cual mostrar (en minutos)
            num_filas: Cantidad de filas a mostrar desde hora_inicio (None = todas)
        
        Returns:
            Lista de filas del vector de estado + última fila
        """
        # Filtrar filas desde hora_inicio
        filas_filtradas = [f for f in self.vector_estado if f.reloj >= hora_inicio]
        
        if num_filas is not None and len(filas_filtradas) > num_filas:
            # Tomar las primeras num_filas
            resultado = filas_filtradas[:num_filas]
        else:
            resultado = filas_filtradas
        
        # Siempre agregar la última fila si no está incluida
        if self.vector_estado and (not resultado or resultado[-1] != self.vector_estado[-1]):
            resultado.append(self.vector_estado[-1])
        
        return resultado
    
    def simular_multiples_dias(self, num_dias: int):
        """Simula múltiples días y devuelve estadísticas agregadas"""
        resultados = []
        
        for dia in range(num_dias):
            stats = self.simular_dia()
            stats['dia'] = dia + 1
            resultados.append(stats)
        
        return self._calcular_estadisticas_agregadas(resultados)
    
    def _calcular_estadisticas_agregadas(self, resultados):
        """Calcula estadísticas agregadas de múltiples días"""
        if not resultados:
            return {}
        
        recaudaciones = [r['recaudacion'] for r in resultados]
        ganancias = [r['ganancia_neta'] for r in resultados]
        sillas = [r['max_sillas_necesarias'] for r in resultados]
        refrigerios = [r['clientes_con_refrigerio'] for r in resultados]
        
        # Probabilidad de 5 o más refrigerios
        dias_5_o_mas = len([r for r in refrigerios if r >= 5])
        prob_5_o_mas = dias_5_o_mas / len(resultados) if resultados else 0
        
        return {
            'num_dias': len(resultados),
            'recaudacion_promedio': sum(recaudaciones) / len(recaudaciones),
            'recaudacion_min': min(recaudaciones),
            'recaudacion_max': max(recaudaciones),
            'ganancia_promedio': sum(ganancias) / len(ganancias),
            'max_sillas_necesarias': max(sillas),
            'sillas_promedio': sum(sillas) / len(sillas),
            'refrigerios_promedio': sum(refrigerios) / len(refrigerios),
            'prob_5_o_mas_refrigerios': prob_5_o_mas,
            'dias_5_o_mas_refrigerios': dias_5_o_mas,
            'resultados_diarios': resultados
        }
