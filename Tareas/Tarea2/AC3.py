#!/usr/bin/env python
# coding: utf-8

# Daniel Rojo Mata
# Inteligencia Artificial, Semestre 2025-I


# Librerias que se usan 
import pandas as pd

import networkx as nx # type: ignore
import numpy as np
import matplotlib as plt


archivo = "gc_50_7 (1)"
# Se importa la data proporcionada
data = pd.read_csv(archivo, # Se lee el archivo
                    header = None, # Sin encabezados
                    sep = " ", # Separación por espacios
                    names = ['nodos1', 'nodos2'] # Se renombran las columnas
                    )

# Se quita el primer renglón
data = data.drop(index=0).reset_index(drop=True)

# Resetear el índice y convertirlo en una columna para poder diferenciar a los elementos 
#data = data.reset_index(drop=False)
# Se cambia el nombre de la columna
# data = data.rename (columns = {'index' : 'object'} )



#Se define una gráfica
G = nx.Graph()

# Columna 1 de la data
colum1 = list(data.loc[:, "nodos1"])

# Columna 1 de la data
colum2 = list(data.loc[:, "nodos2"])

#Nodos de la gráfica
nodes= np.unique(colum1)

#Aristas de la gráfica
edges = list(zip(colum1, colum2))

#Se agregan los nodos y las aristas
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# Se visualiza la gráfica
nx.draw_kamada_kawai(G)




# Este es el dominio de cada nodo
domain = ["red", "blue", "green", "yellow"]

#Se hace un diccionario en donde cada nodo tiene un dominio asociado, en este caso, 4 colores
grafica = {
    node: domain for node in nodes
}

# La restricción es que haya dos colores distintos 

domain2 = ["red", "blue", "green", "yellow"]

# xi, xj son nodos de la gráfica
# (xi, xj) representan las aristas de la gráfica

# def revise(xi, xj):
# # En este caso xi, xj, son las etiquetas de los nodos, i.e.
# # xi = 1, xj = 2, etc
    
#     #contadores para ir recorriendo los elementos del dominio
#     i = 0
#     j = 0
#     # contador que ayuda a saber si es que hay elementos o no 
#     # tales que "x" se relaciona con "y"
#     k = 0
    
#     revised = False
    
#     # Longitud del dominio, que es la misma para todos los elementos
#     n = len(grafica[xi])
    
    
#     while i < n and j < n:
#         if grafica[xi][i] == grafica[xj][j]:
#             j += 1 
#         else:
#             k += 1
#             i += 1
#             j = 0

#     if k >= n:
#         revised = True
    
#     return revised

# xi = 0
# xj = 1 

def revise(xi, xj):
    # Verificar que ambos nodos están en la gráfica
    if xi not in grafica or xj not in grafica:
        return False
    
    n = len(grafica[xi])
    m = len(grafica[xj])  # Longitud de grafica[xj]
    
    nuevo_dominio = []
    
    revised = False
    
    for i in range(0, n-1):
        contador = 0
        for j in range(0, m-1): 
            if grafica[xi][i] != grafica[xj][j]:
                nuevo_dominio.append(grafica[xj][j])
                break
            else:
                contador += 1                 

        if contador == m:
            grafica[xi] = nuevo_dominio
            revised = True
            break
    
    return revised


def AC3(grafica, edges):
    # Se define una cola en donde se añaden los elemntos 
    queue = [arista for arista in edges]

    # Mientras la cola no sea vacía
    while queue:
        # Saco el primer elemento de la cola
        (xi, xj) = queue.pop(0)
        # Si revise(xi, xj) es true, entonces:
        if revise(xi,xj, grafica):
            if len(grafica[xi]) == 0:
                return False

            for xk in [n for n in G.neighbors(xi) if n != xj]:
                queue.insert(0,(xk,xi))
    return True


AC3(grafica, edges)