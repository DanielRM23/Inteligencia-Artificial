#!/usr/bin/env python
# coding: utf-8

# Daniel Rojo Mata
# Inteligencia Artificial, Semestre 2025-I

# Librerias que se usan 
import pandas as pd
import heapq


def mochila(archivo, peso):

    # Se importa la data proporcionada
    data = pd.read_csv(archivo, # Se lee el archivo
                      header = None, # Sin encabezados
                      sep = " ", # Separación por espacios
                      names = ['costos', 'pesos'] # Se renombran las columnas
                      )

    # Se quita el primer renglón
    data = data.drop(index=0).reset_index(drop=True)

    # Resetear el índice y convertirlo en una columna para poder diferenciar a los elementos 
    data = data.reset_index(drop=False)
    # Se cambia el nombre de la columna
    data = data.rename (columns = {'index' : 'object'} )

    # Se calcula la heurística para cada objeto, siendo ésta: h = peso/costo
    data['h'] = data['costos'] / data['pesos']
    
    # Se crea un diccionario donde key es el objeto y value es una tupla (costo, peso, heuristica)
    diccionario_original = {
        obj: (costo, peso, heuristica)
        for obj, costo, peso, heuristica in zip(data['object'], data['costos'], data['pesos'], data['h'])
    }

    # Ordenar el diccionario por heurísticas en orden descendente
    diccionario_ordenado = dict(sorted(diccionario_original.items(),
                                       key=lambda item: item[1][2],
                                       reverse=True))
    # Límite de peso
    peso_limit = peso

    # Aplicar enfoque greedy
    items_seleccionados = {}
    valor_total = 0
    peso_total = 0

    for item_id, (costo, peso, heuristica) in diccionario_ordenado.items():
        # Itera sobre cada elemento en el diccionario ordenado.
        # 'item_id' es la clave del diccionario, mientras que 'costo', 'peso', y 'heuristica' son los valores.

        if peso_total + peso <= peso_limit:
            # Comprueba si al agregar el peso del elemento actual al peso total no se supera el límite de peso (peso_limit).

            items_seleccionados[item_id] = (costo, peso)
            # Si la condición anterior se cumple, agrega el elemento seleccionado al diccionario 'items_seleccionados'.
            # La clave es 'item_id' y el valor es una tupla con el 'costo' y 'peso' del elemento.

            valor_total += costo
            # Suma el 'costo' del elemento actual al 'valor_total'.

            peso_total += peso
            # Suma el 'peso' del elemento actual al 'peso_total'.

        else:
            continue
        # Si agregar el peso del elemento actual excede el límite de peso, pasa al siguiente elemento en el bucle sin hacer nada.


    # Mostrar resultados
    print("Items seleccionados:", items_seleccionados)
    print("Valor total:", valor_total)
    print("Peso total:", peso_total)
    

print("Mochila con 19 elementos: \n")
# Se importan los datos
archivo = "ks_19_0"
peso = 31181
mochila(archivo, peso)

print("\n----------------------------------------------------------------\n")

print("Mochila con 10,000 elementos: \n")
# Se importan los datos
archivo = "ks_10000_0"
peso = 1000000

mochila(archivo, peso)

