#!/usr/bin/env python
# coding: utf-8




# Librerías que se usan
import pandas as pd
import networkx as nx  # type: ignore
import numpy as np
import matplotlib.pyplot as plt


# Función para limpiar y procesar la data del archivo
def limpiar_data(archivo):
    # Se importa la data proporcionada
    data = pd.read_csv(archivo,  # Se lee el archivo
                       header=None,  # Sin encabezados
                       sep=" ",  # Separación por espacios
                       names=['nodos1', 'nodos2']  # Se renombran las columnas
                       )

    # Se quita el primer renglón
    data = data.drop(index=0).reset_index(drop=True)
    
    # Columna 1 de la data
    colum1 = list(data.loc[:, "nodos1"])

    # Columna 2 de la data
    colum2 = list(data.loc[:, "nodos2"])

    # Nodos de la gráfica, se asegura que sean únicos 
    nodes = np.unique(colum1)

    # Aristas de la gráfica
    edges = list(zip(colum1, colum2))
    
    return nodes, edges



# Función para crear la gráfica usando NetworkX
def grafica(archivo, numero_colores):
    nodes, edges = limpiar_data(archivo)
    
    # Se define una gráfica
    G = nx.Graph()

    # Se agregan los nodos y las aristas
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # Dominio de cada nodo, es decir, los colores
    domain = [_ for _ in range(numero_colores)]

    # Se hace un diccionario donde cada nodo en G tiene un dominio asociado
    Grafica = {node: domain[:] for node in G.nodes()}  # Usar G.nodes() para asegurar que todos los nodos estén incluidos

    return Grafica, G



# Función AC3 para reducir los dominios
def ac3(Grafica, G):
    # Inicializa la cola con todos los arcos del CSP
    queue = [(v, w) for v in G.nodes() for w in G.neighbors(v)]
    
    while queue:
        (v, w) = queue.pop(0)
        if revise(Grafica, v, w):
            if len(Grafica[v]) == 0:
                return False  # No hay solución si un dominio queda vacío
            for u in G.neighbors(v):
                if u != w:
                    queue.append((u, v))
    return True



# Función revise para eliminar valores inconsistentes en el dominio
def revise(Grafica, v, w):
    revised = False
    for color in Grafica[v][:]:
        if all(color == otro_color for otro_color in Grafica[w]):
            Grafica[v].remove(color)
            revised = True
    return revised



def select_unassigned_variable(asignacion, Grafica):
    # Encuentra las variables (nodos) que aún no han sido asignadas en el CSP.
    unassigned = [v for v in Grafica if v not in asignacion]
    
    # Utiliza la heurística MRV (Minimum Remaining Values) para seleccionar la variable
    # no asignada con el dominio más pequeño. La idea es elegir la variable más restringida
    # primero, lo que puede reducir el espacio de búsqueda.
    return min(unassigned, key=lambda var: len(Grafica[var]))



def es_consistente(var, value, asignacion, G):
    # Verifica si la asignación actual de la variable `var` con el valor `value`
    # es consistente con las restricciones del problema.
    
    # Itera sobre los vecinos de la variable `var` en el grafo `G`.
    for vecino in G.neighbors(var):
        # Si el vecino ya tiene asignado un valor y ese valor es igual al `value`
        # que se intenta asignar a `var`, entonces la asignación no es consistente
        # (dos nodos adyacentes no pueden tener el mismo color).
        if vecino in asignacion and asignacion[vecino] == value:
            return False
    
    # Si no se encontró ningún conflicto, la asignación es consistente.
    return True



def backtracking(asignacion, Grafica, G):
    # Si todas las variables (nodos) han sido asignadas, es decir, si la longitud de la asignación
    # es igual al número total de nodos en el grafo, entonces se ha encontrado una solución completa
    # y se devuelve la asignación.
    if len(asignacion) == len(Grafica):
        return asignacion
    
    # Selecciona la siguiente variable (nodo) no asignada usando la heurística MRV (Minimum Remaining Values).
    # La función `select_unassigned_variable` selecciona la variable con el dominio más pequeño para reducir el
    # espacio de búsqueda.
    var = select_unassigned_variable(asignacion, Grafica)
    
    # Recorre todos los valores posibles (colores) en el dominio de la variable seleccionada `var`.
    for value in Grafica[var]:
        # Verifica si asignar el valor `value` a la variable `var` es consistente con las restricciones del problema,
        # es decir, que no haya conflictos con los vecinos en el grafo.
        if es_consistente(var, value, asignacion, G):
            # Si la asignación es consistente, se asigna el valor `value` a la variable `var`.
            asignacion[var] = value
            
            # Llama recursivamente a la función `backtracking` para continuar con la búsqueda
            # en el siguiente nodo. Si se encuentra una solución válida, se devuelve.
            result = backtracking(asignacion, Grafica, G)
            if result:
                return result  # Solución encontrada
            
            # Si no se encuentra una solución después de asignar `value` a `var`,
            # se deshace la asignación (backtracking) y se prueba con otro valor.
            del asignacion[var]
    
    # Si se han probado todos los valores y ninguno funciona, se devuelve `None`,
    # lo que indica que no hay solución posible desde el estado actual de la asignación.
    return None  # No hay solución



# Función de búsqueda por backtracking
def backtracking_search(Grafica, G):
    return backtracking({}, Grafica, G)



# Función principal para resolver el problema de coloreado de grafos con AC3
def coloreado(archivo, numero_colores):
    # Crear la gráfica y sus dominios
    Grafica, G = grafica(archivo, numero_colores)
    
    # Ejecutar AC3 para reducir los dominios
    if ac3(Grafica, G):
        # Búsqueda para encontrar la asignación de colores
        solucion = backtracking_search(Grafica, G)
        return solucion
    else:
        return None  # No hay solución

    

# función que manda a llamar todo
def coloreado_Mapa(archivo, numero_colores):
    solution = coloreado(archivo, numero_colores)

    if solution:
        print("Solución encontrada:")
        for node, color in solution.items():
            print(f"Nodo {node}: Color {color}")
    else:
        print("No existe una solución.")




#50 nodos:
archivo_50 = "gc_50_7 (1)" 
numero_colores_50 = 15

coloreado_Mapa(archivo_50, numero_colores_50)

#1000 nodos:
# archivo_1000 = "gc_1000_9 (1)" 
# numero_colores_1000 = 500

# coloreado_Mapa(archivo_1000, numero_colores_1000)
