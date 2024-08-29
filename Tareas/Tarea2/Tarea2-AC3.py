#!/usr/bin/env python
# coding: utf-8


# Daniel Rojo Mata
# Inteligencia Artificial, Semestre 2025-I

# Librerias que se usan 
import pandas as pd
import heapq


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


import networkx as nx # type: ignore
import numpy as np
import matplotlib as plt




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
diccionario = {
    node: domain for node in nodes
}

# La restricción es que haya dos colores distintos 

domain2 = ["red", "blue", "green", "yellow"]




print(diccionario)






