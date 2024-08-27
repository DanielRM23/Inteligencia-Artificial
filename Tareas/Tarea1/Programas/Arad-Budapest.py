#!/usr/bin/env python
# coding: utf-8

# Daniel Rojo Mata
# Inteligencia Artificial, Semestre 2025-I

# Problema de Arad a Budapest

# Se importa para usar heaps
import heapq


# Se utiliza un diccionario como estructura de datos para representar la gráfica
# diccionario = { ciudad : {vecino : [costo_para_ir_a_vecino, heuristica_ciudad] }}
    # Las claves son los nombres de las ciudades.
    # Los valores son diccionarios que representan las ciudades vecinas.
    # Para cada vecino, la lista contiene dos elementos: el costo (distancia) y la heurística hacia Bucarest.

# Gráfica representada como un diccionario de adyacencias
# Las heurísticas son las distancias euclideánas entre las ciudades. Éstas fueron obtenidas del libro
# Artificial Intelligence: A modern Approach, 3rd Edition, pagina 93.
grafica = {
    "Arad": { "Zerind": [75, 374], "Timisoara": [118, 329], "Sibiu": [140, 253] },
    "Zerind": { "Arad": [75, 366], "Oradea": [71, 380] },
    "Oradea": { "Zerind": [71, 374], "Sibiu": [151, 253] },
    "Timisoara": { "Arad": [118, 366], "Lugoj": [111, 244] },
    "Lugoj": { "Timisoara": [111, 329], "Mehadia": [70, 241] },
    "Mehadia": { "Lugoj": [70, 244], "Drobeta": [75, 242] },
    "Drobeta": { "Mehadia": [75, 241], "Craiova": [120, 160] },
    "Craiova": { "Drobeta": [120, 242], "Rimnicu Vilcea": [146, 193], "Pitesti": [138, 100] },
    "Sibiu": { "Arad": [140, 366], "Oradea": [151, 380], "Fagaras": [99, 176], "Rimnicu Vilcea": [80, 193] },
    "Rimnicu Vilcea": { "Sibiu": [80, 253], "Craiova": [146, 160], "Pitesti": [97, 100] },
    "Fagaras": { "Sibiu": [99, 253], "Bucarest": [211, 0] },
    "Pitesti": { "Rimnicu Vilcea": [97, 193], "Craiova": [138, 160], "Bucarest": [101, 0] },
    "Bucarest": { "Fagaras": [211, 176], "Pitesti": [101, 100], "Giurgiu": [90, 77], "Urziceni": [85, 80] },
    "Giurgiu": { "Bucarest": [90, 0] },
    "Urziceni": { "Bucarest": [85, 0], "Hirsova": [98, 151], "Vaslui": [142, 199] },
    "Hirsova": { "Urziceni": [98, 80], "Eforie": [86, 161] },
    "Eforie": { "Hirsova": [86, 151] },
    "Vaslui": { "Urziceni": [142, 80], "Iasi": [92, 226] },
    "Iasi": { "Vaslui": [92, 199], "Neamt": [87, 234] },
    "Neamt": { "Iasi": [87, 226] }
}



def a_star(grafica, inicio, meta):
    # Inicializar la cola de prioridad (openSet)
    cola_prioridad = []
    
    # Al principio, no se conoce el costo del camino desde el nodo inicial hasta los demás nodos del grafo, 
    # excepto para el nodo inicial (que es 0). Por lo tanto, se asume que el costo es
    # "infinitamente grande" hasta que se encuentre un camino mejor.
    # Este valor representa la idea de que, inicialmente, no hay un camino conocido hacia esos nodos.
    # Esta es la razón del porqué se incicializan algunos valores con float('inf')
    
    # Obtener la heurística inicial del nodo de inicio hacia la meta
    heuristica_inicial = grafica[inicio].get(meta, [0, float('inf')])[1]
    # Insertar el nodo inicial en la cola de prioridad junto con su heurística
    heapq.heappush(cola_prioridad, (heuristica_inicial, inicio))
    
    # Rastrear el camino más eficiente hacia cada nodo
    camino = {}  
    
    # Inicializar g(n), que representa el costo total desde el nodo inicial hasta el nodo actual
    g_values = {nodo: float('inf') for nodo in grafica} 
    # El costo del nodo inicial es 0
    g_values[inicio] = 0  
    
    # Inicializar f(n), que representa el costo estimado total desde el nodo inicial hasta la meta,
    # pasando por el nodo actual (f(n) = g(n) + h(n))
    f_values = {nodo: float('inf') for nodo in grafica}
    # Para el nodo inicial, f(n) = h(n), ya que g(n) = 0
    f_values[inicio] = grafica[inicio].get(meta, [0, float('inf')])[1]  
    
    # Mientras la cola de prioridad no esté vacía:
    while cola_prioridad:
        # Obtener el nodo con el menor valor f(n)
        actual = heapq.heappop(cola_prioridad)[1]
        
        # Si llegamos al objetivo (meta), reconstruir el camino y devolverlo
        if actual == meta:
            return camino_final(camino, actual)
        
        # Explorar los vecinos del nodo actual
        # La gráfica se modela como un diccionario donde cada nodo tiene como valor un diccionario
        # de vecinos con sus costos y heurísticas
        for vecino, (costo, heuristica) in grafica[actual].items():
            # Calcular g_tentativo, que es el costo total desde el nodo inicial hasta el vecino,
            # pasando por el nodo actual
            g_tentativo = g_values[actual] + costo
            
            # Si encontramos un camino más corto hacia el vecino
            if g_tentativo < g_values[vecino]:
                # Actualizar el camino óptimo hacia el vecino
                camino[vecino] = actual
                g_values[vecino] = g_tentativo
                # Calcular f(n) para el vecino
                f_values[vecino] = g_values[vecino] + heuristica
                
                # Añadir el vecino a la cola de prioridad si aún no está presente
                if vecino not in [i[1] for i in cola_prioridad]:
                    heapq.heappush(cola_prioridad, (f_values[vecino], vecino))
    
    # Si no se encuentra un camino hacia la meta, devolver None
    return None

def camino_final(camino, actual):
    # Reconstruir el camino desde la meta hacia el inicio
    camino_total = [actual]
    while actual in camino:
        actual = camino[actual]
        camino_total.append(actual)
    # Invertir el camino para obtenerlo desde el inicio hasta la meta
    return camino_total[::-1]

# Ejemplo de uso del algoritmo A* para el problema de "Arad-Budapest"
inicio = 'Arad'
meta = 'Bucarest'
path = a_star(grafica, inicio, meta)
print("Camino encontrado:", path)
