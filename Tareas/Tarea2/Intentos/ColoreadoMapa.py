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
def grafica(archivo):
    nodes, edges = limpiar_data(archivo)
    
    # Se define una gráfica
    G = nx.Graph()

    # Se agregan los nodos y las aristas
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # Dominio de cada nodo, es decir, los colores
    domain = [_ for _ in range(18)]

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


# Función de búsqueda por backtracking
def backtracking_search(Grafica, G):
    return backtracking({}, Grafica, G)


def backtracking(asignacion, Grafica, G):
    # Si todas las variables están asignadas, devolver la asignación
    if len(asignacion) == len(Grafica):
        return asignacion
    
    # Selecciona la variable no asignada con el dominio más pequeño (heurística MRV)
    var = select_unassigned_variable(asignacion, Grafica)
    
    for value in Grafica[var]:
        if es_consistente(var, value, asignacion, G):
            # Asigna el valor a la variable
            asignacion[var] = value
            result = backtracking(asignacion, Grafica, G)
            if result:
                return result
            # Si falla, deshace la asignación
            del asignacion[var]
    
    return None  # No hay solución


def select_unassigned_variable(asignacion, Grafica):
    unassigned = [v for v in Grafica if v not in asignacion]
    return min(unassigned, key=lambda var: len(Grafica[var]))


def es_consistente(var, value, asignacion, G):
    # Verifica que la asignación sea consistente con las restricciones
    for vecino in G.neighbors(var):
        if vecino in asignacion and asignacion[vecino] == value:
            return False
    return True


# Función principal para resolver el problema de coloreado de grafos con AC3
def coloreado(archivo):
    # Crear la gráfica y sus dominios
    Grafica, G = grafica(archivo)
    
    # Ejecutar AC3 para reducir los dominios
    if ac3(Grafica, G):
        # Búsqueda para encontrar la asignación de colores
        solucion = backtracking_search(Grafica, G)
        return solucion
    else:
        return None  # No hay solución


# Ejemplo de uso:
archivo = "gc_50_7 (1)"  # Reemplaza con el nombre de tu archivo
solution = coloreado(archivo)

if solution:
    print("Solución encontrada:")
    for node, color in solution.items():
        print(f"Nodo {node}: Color {color}")
else:
    print("No existe una solución.")
