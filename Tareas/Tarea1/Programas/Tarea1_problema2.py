import pandas as pd


# Se importan los datos
arcihvo = "ks_19_0"
data = pd.read_csv(arcihvo, 
                  header = None,
                  sep = " ",
                  names = ['costs', 'weights']
                  )

# Quito el primer renglón
data = data.drop(index=0).reset_index(drop=True)

# Resetear el índice y convertirlo en una columna para poder diferenciar a los elementos 
data = data.reset_index(drop=False)
# Cambio el nombre de la columna
data = data.rename (columns = {'index' : 'object'} )

# Se calcula la heurística para cada objeto, siendo ésta: h = weight/cost
data['h'] = data['costs'] / data['weights']

print(data)


# Crear un diccionario donde key es el objeto y value es la heurística
diccionario_original = dict(zip(data['object'], data['h']))

# Ordenar el diccionario por valores (heurística) en orden descendente
diccionario_ordenado = dict(sorted(diccionario_original.items(),
                                   key=lambda item: item[1],
                                   reverse=True))


print(diccionario_ordenado)