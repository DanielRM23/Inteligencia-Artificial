#!/usr/bin/env python
# coding: utf-8

# Daniel Rojo Mata
# Inteligencia Artificial, Semestre 2025-I


# Librerias que se usan 
import pandas as pd

# Se usa principalmente para obtener infomación de la gráfica
import networkx as nx # type: ignore
import numpy as np
import matplotlib as plt


def limpiar_data(archivo):
    # Archivos que contienen la data
    # Se importa la data proporcionada
    data = pd.read_csv(archivo, # Se lee el archivo
                        header = None, # Sin encabezados
                        sep = " ", # Separación por espacios
                        names = ['nodos1', 'nodos2'] # Se renombran las columnas
                        )

    # Se quita el primer renglón
    data = data.drop(index=0).reset_index(drop=True)
    # Columna 1 de la data
    colum1 = list(data.loc[:, "nodos1"])
    # Columna 2 de la data
    colum2 = list(data.loc[:, "nodos2"])
    #Nodos de la gráfica, se asegura que sean únicos 
    nodes= np.unique(colum1)
    #Aristas de la gráfica
    edges = list(zip(colum1, colum2))
    
    return nodes, edges
    

def grafica(archivo):
    nodes, edges = limpiar_data(archivo)
    #Se define una gráfica
    G = nx.Graph()
    #Se agregan los nodos y las aristas
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)

    # Este es el dominio de cada nodo
    # La restricción es que dos nodos adyacentes xi, xj no tengan el mismo color
    domain = ["red", "blue", "green", "yellow"]

    #Se hace un diccionario en donde cada nodo tiene un dominio asociado, en este caso, 4 colores
    Grafica = {
        node: domain for node in nodes
    }

    return Grafica, G


def revise(grafica, xi, xj):
    # Verificar que ambos nodos están en la gráfica
    if xi not in grafica or xj not in grafica:
        return False

    # Obtener el tamaño de los dominios de los nodos xi y xj
    n = len(grafica[xi])
    m = len(grafica[xj])
    # Lista para almacenar el nuevo dominio de xi
    nuevo_dominio = []
    
    # Bandera para indicar si el dominio de xi ha sido revisado
    revised = False
    
    # Iterar sobre cada valor en el dominio de xi
    for xi_val in grafica[xi]:
        valido = False  # Bandera para verificar si xi_val es válido
        # Verificar si xi_val es diferente de al menos un valor en el dominio de xj
        for xj_val in grafica[xj]:
            if xi_val != xj_val:
                valido = True  # xi_val es válido si es diferente de xj_val
                break  # Salir del bucle interno si se encuentra un valor válido
        # Si xi_val es válido, añadirlo al nuevo dominio
        if valido:
            nuevo_dominio.append(xi_val)
        else:
            # Si xi_val no es válido para ningún valor en el dominio de xj, marcar como revisado
            revised = True

    # Si el dominio de xi ha sido modificado, actualizarlo en la gráfica
    if revised:
        grafica[xi] = nuevo_dominio

    # Retornar True si el dominio de xi ha sido revisado, False en caso contrario
    return revised


def AC3(grafica, G):
    # Se define una cola en donde se añaden los elemntos 
    edges = list(G.edges())
    queue = [arista for arista in edges]

    # Mientras la cola no sea vacía
    while queue:
        # Saco el primer elemento de la cola
        xi, xj = queue.pop(0)
        # Si revise(xi, xj) es true, entonces:
        if revise(grafica, xi, xj):
            if len(grafica[xi]) == 0:
                return False

            for xk in [n for n in G.neighbors(xi) if n != xj]:
                queue.insert(0,(xk,xi))
    return True

#------------------------------------------------------------------------------

print("Verificación para 50 nodos")
# Nombre del archivo CSV (asegúrate de incluir la extensión .csv)
archivo_50 = "gc_50_7 (1)"
# Obtener el diccionario de dominios y el grafo
grafica_50, G_50 = grafica(archivo_50)
# Llamar a AC3 con los argumentos adecuados
resultado = AC3(grafica_50, G_50)
# Imprimir el resultado
print(resultado)

# -----------------------------------------------------------------------------
print("Verificación para 1000 nodos")
# Nombre del archivo CSV (asegúrate de incluir la extensión .csv)
archivo_1000 = "gc_1000_9 (1)"
# Obtener el diccionario de dominios y el grafo
grafica_1000, G_1000 = grafica(archivo_1000)
# Llamar a AC3 con los argumentos adecuados
resultado = AC3(grafica_1000, G_1000)

# Imprimir el resultado
print(resultado)