#!/usr/bin/env python
# coding: utf-8

# Daniel Rojo Mata
# Inteligencia Artificial, Semestre 2025-I

# Problema de coloreado de Grafo usando BackTracking, Revisión hacia adelante y Ac3


# Librerías que se usan
import pandas as pd
import networkx as nx  # type: ignore
import numpy as np

# Función para limpiar y procesar la data del archivo
def limpiar_data(archivo):
    data = pd.read_csv(archivo,  # Se lee el archivo
                       header=None,  # Sin encabezados
                       sep=" ",  # Separación por espacios
                       names=['nodos1', 'nodos2']  # Se renombran las columnas
                       )
    data = data.drop(index=0).reset_index(drop=True)
    
    colum1 = list(data.loc[:, "nodos1"])
    colum2 = list(data.loc[:, "nodos2"])
    nodes = np.unique(colum1)
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
    queue = [(v, w) for v in G.nodes() for w in G.neighbors(v)]
    
    while queue:
        (v, w) = queue.pop(0)
        if revise(Grafica, v, w):
            if len(Grafica[v]) == 0:
                return False
            for u in G.neighbors(v):
                if u != w:
                    queue.append((u, v))
    return True



# Función revise para eliminar valores inconsistentes en el dominio
def revise(Grafica, v, w):
    revised = False
    for color in Grafica[v][:]:
        if all(color == other_color for other_color in Grafica[w]):
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



# Función Forward Checking para reducir dominios
def forward_checking(asignacion, Grafica, G):
    # Recorre todas las variables en el grafo
    for var in Grafica:
        # Solo considera las variables que aún no han sido asignadas
        if var not in asignacion:
            # Filtra el dominio de la variable `var` para eliminar valores que no son consistentes
            # con la asignación actual. Se mantiene solo los colores válidos.
            Grafica[var] = [color for color in Grafica[var] if es_consistente(var, color, asignacion, G)]
            
            # Si después de la eliminación, el dominio de `var` queda vacío,
            # significa que no hay colores válidos para `var` dado el estado actual
            # de la asignación, lo que implica que la asignación actual no es válida.
            if not Grafica[var]:
                return False  # La asignación es inconsistente
    
    # Si todos los dominios siguen siendo válidos (no vacíos), la asignación actual
    # es consistente y se puede continuar con la búsqueda.
    return True



# Función de búsqueda por backtracking con Forward Checking
def backtracking(asignacion, Grafica, G):
    # Verifica si todas las variables (nodos) han sido asignadas
    # Si la longitud de `asignacion` es igual al número de nodos en `Grafica`, significa que
    # hemos encontrado una solución completa, así que devolvemos la asignación.
    if len(asignacion) == len(Grafica):
        return asignacion
    
    # Selecciona la siguiente variable (nodo) que no ha sido asignada utilizando la heurística MRV
    # `select_unassigned_variable` escoge la variable con el dominio más pequeño.
    var = select_unassigned_variable(asignacion, Grafica)
    
    # Recorre todos los valores posibles (colores) en el dominio de la variable `var`.
    for value in Grafica[var]:
        # Verifica si la asignación del valor `value` a la variable `var` es consistente con las restricciones
        # del problema, es decir, si no entra en conflicto con las asignaciones actuales.
        if es_consistente(var, value, asignacion, G):
            # Si la asignación es consistente, se asigna el valor `value` a la variable `var`.
            asignacion[var] = value
            
            # Aplica Forward Checking para reducir el dominio de las variables no asignadas
            # y asegurarse de que la asignación actual no lleva a un dominio vacío.
            if forward_checking(asignacion, Grafica, G):
                # Llama recursivamente a `backtracking` para continuar con la búsqueda de la solución.
                result = backtracking(asignacion, Grafica, G)
                if result:
                    return result  # Si se encuentra una solución válida, la devolvemos.
            
            # Si la asignación actual no lleva a una solución válida, se deshace la asignación
            # (se realiza el backtracking) y se prueba con el siguiente valor en el dominio.
            del asignacion[var]
    
    # Si se han probado todos los valores posibles para la variable `var` y ninguno lleva a una solución,
    # se devuelve `None`, indicando que no hay solución desde el estado actual de la asignación.
    return None



# Función principal para resolver el problema de coloreado de grafos con AC3 y Forward Checking
def coloreado_ac3_forward_checking(archivo, numero_colores):
    Grafica, G = grafica(archivo, numero_colores)
    if ac3(Grafica, G):
        solution = backtracking({}, Grafica, G)
        return solution
    else:

        return None

    

# # función que manda a llamar todo
# # Esta función solo imprime en pantalla los nodos con los colores 
# def coloreado_Mapa(archivo, numero_colores):
    
#     solution = coloreado_ac3_forward_checking(archivo, numero_colores)

#     if solution:
#         print("Solución encontrada:")
#         for node, color in solution.items():
#             print(f"Nodo {node}: Color {color}")
#     else:
#         print("No existe una solución.")


# Función que manda a llamar todo y presenta la solución en un DataFrame de pandas
def coloreado_Mapa(archivo, numero_colores):
    solution = coloreado_ac3_forward_checking(archivo, numero_colores)

    if solution:
        print("Solución encontrada:")
        # Ordenar los nodos y sus colores
        df_solucion = pd.DataFrame(sorted(solution.items()), columns=['Nodo', 'Color'])
        print(df_solucion)
    else:
        print("No existe una solución.")



# ------------------ EJECUCIÓN ------------------------


#------- 50 nodos ----------

# archivo_50 = "gc_50_7 (1)" 
# numero_colores_50 = 16

# coloreado_Mapa(archivo_50, numero_colores_50)


#------- 1000 nodos ----------

archivo_1000 = "gc_1000_9 (1)" 
numero_colores_1000 = 929

coloreado_Mapa(archivo_1000, numero_colores_1000)
