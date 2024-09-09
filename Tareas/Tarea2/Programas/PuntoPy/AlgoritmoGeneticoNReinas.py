#!/usr/bin/env python
# coding: utf-8



import random

def tableros(n, m):
    '''
    Función que genera m números aleatorios entre 1 y n (incluidos) sin repetirlos.
    
    Parámetros:
    n (int): Valor máximo del rango (incluido).
    m (int): Cantidad de números aleatorios a generar.

    Retorna:
    list: Lista de números aleatorios sin repetición.
    '''
    if m > n:
        raise ValueError("m no puede ser mayor que n.")
    return random.sample(range(1, n+1), m)



def fit(tablero):
    '''
    Función que cuenta el número de ataques posibles entre las reinas, 
    los ataques no son contados dobles 
    '''
    
    ataques = 0 #contador de ataques 
    n = len(tablero) 
    
    # Diccionarios para contar reinas en diagonales principales y secundarias
    diagonal_principal = {}
    diagonal_secundaria = {}
    
    for i in range(n):
        fila = tablero[i]
        columna = i
        
        dp = fila - columna  # Diagonal principal
        ds = fila + columna  # Diagonal secundaria
        
        # Contar ataques en diagonal principal
        if dp in diagonal_principal:
            ataques += diagonal_principal[dp]
            diagonal_principal[dp] += 1
        else:
            diagonal_principal[dp] = 1
        
        # Contar ataques en diagonal secundaria
        if ds in diagonal_secundaria:
            ataques += diagonal_secundaria[ds]
            diagonal_secundaria[ds] += 1
        else:
            diagonal_secundaria[ds] = 1
    
    return ataques



def generar_poblacion_inicial(tamano_poblacion, n):
    '''
    Función para generar una población inicial de tableros.
    
    Parámetros:
    tamano_poblacion (int): Número de tableros a generar.
    n (int): Tamaño del tablero (n x n).

    Retorna:
    list: Lista de tableros generados.
    '''
    return [tableros(n, n) for _ in range(tamano_poblacion)]



def ordenar_poblacion(poblacion):
    '''
    Función que ordena la población de tableros según el valor de ajuste (fitness).
    
    Parámetros:
    poblacion (list): Lista de tableros.

    Retorna:
    dict: Diccionario ordenado por el valor de ajuste (fitness).
    '''
    # Crear un diccionario con índice como clave y (tablero, valor_fit) como valor
    tableros_fit = {i: (tablero, fit(tablero)) for i, tablero in enumerate(poblacion)}
    
    # Ordenar el diccionario por el valor menor de fit
    tableros_fit_ordenado = dict(sorted(tableros_fit.items(), key=lambda item: item[1][1]))
    return tableros_fit_ordenado



def cruza_permutacion(tablero1, tablero2):
    '''
    Puntos de Corte: Se eligen dos puntos de corte aleatorios en el tablero.
    Copiar Segmentos: Se copian los segmentos entre los puntos de corte de los tableros padres a los hijos.
    Completar Hijos: Se completan los hijos con los números faltantes de los tableros padres para asegurar 
    que todos los números del tablero estén presentes y sean únicos.
    '''
    n = len(tablero1)
    hijo1 = [-1] * n
    hijo2 = [-1] * n
    
    # Elegir puntos de corte para la permutación
    punto_corte1, punto_corte2 = sorted(random.sample(range(n), 2))
    
    # Copiar segmentos de los padres a los hijos
    hijo1[punto_corte1:punto_corte2] = tablero1[punto_corte1:punto_corte2]
    hijo2[punto_corte1:punto_corte2] = tablero2[punto_corte1:punto_corte2]
    
    def completar_hijo(hijo, otro_padre):
        falta = [x for x in otro_padre if x not in hijo]
        indice = 0
        for i in range(n):
            if hijo[i] == -1:
                hijo[i] = falta[indice]
                indice += 1
    
    completar_hijo(hijo1, tablero2)
    completar_hijo(hijo2, tablero1)
    
    return hijo1, hijo2



def mutacion(tablero):
    '''
    Elegir Posiciones: Se seleccionan dos posiciones aleatorias en el tablero.
    Intercambiar Valores: Los valores en estas dos posiciones se intercambian.
    '''
    n = len(tablero)
    
    # Elegir dos posiciones aleatorias para intercambiar
    pos1, pos2 = random.sample(range(n), 2)
    
    # Intercambiar las posiciones de las reinas
    tablero[pos1], tablero[pos2] = tablero[pos2], tablero[pos1]
    
    return tablero



def seleccionar_padres(poblacion_ordenada, tamaño_torneo=3):
    """
    Selecciona dos padres utilizando el método de torneo.
    
    Parámetros:
    poblacion_ordenada (dict): Diccionario de tableros ordenados por fitness.
    tamaño_torneo (int): Número de individuos en el torneo para la selección.

    Retorna:
    tupla: Dos tableros seleccionados como padres.
    """
    # Extraer los valores (tablero, fit) del diccionario
    individuos = list(poblacion_ordenada.values())
    
    # Seleccionar un torneo de tamaño_torneo individuos
    torneo = random.sample(individuos, tamaño_torneo)
    
    # Seleccionar el mejor individuo del torneo
    mejor_padre1 = min(torneo, key=lambda x: x[1])
    torneo.remove(mejor_padre1)
    mejor_padre2 = min(torneo, key=lambda x: x[1])
    
    return mejor_padre1[0], mejor_padre2[0]



def evolucionar(poblacion_ordenada, tamano_poblacion, max_generaciones):
    
    #contadores 
    num_generaciones = 0
    mejor_solucion = None
    mejor_fit = float('inf')  # Inicializar con infinito positivo
    
    # Se inicia el ciclo de generaciones 
    while num_generaciones < max_generaciones:
        nueva_poblacion = []

        while len(nueva_poblacion) < tamano_poblacion:
            # Seleccionar dos padres
            padre1, padre2 = seleccionar_padres(poblacion_ordenada)
            
            # Cruza los padres para obtener dos hijos
            hijo1, hijo2 = cruza_permutacion(padre1, padre2)
            
            # Aplica mutación a los hijos
            hijo1 = mutacion(hijo1)
            hijo2 = mutacion(hijo2)
            
            nueva_poblacion.extend([hijo1, hijo2])
        
        # Mantener el tamaño de la población
        nueva_poblacion = nueva_poblacion[:tamano_poblacion]
        
        # Ordenar la nueva población
        poblacion_nueva_ordenada = ordenar_poblacion(nueva_poblacion)
        
        # Verificar si hay un tablero con fit = 0
        for _, (tablero, valor_fit) in poblacion_nueva_ordenada.items():
            if valor_fit == 0:
                print(f"\n Tablero encontrado con fit = 0: {tablero}")
                return tablero, valor_fit  # Retorna el tablero y su ajuste óptimo
        
        # Actualizar la mejor solución hasta ahora
        mejor_tablero_actual, mejor_fit_actual = next(iter(poblacion_nueva_ordenada.values()))
        if mejor_fit_actual < mejor_fit:
            mejor_solucion = mejor_tablero_actual
            mejor_fit = mejor_fit_actual
        
        poblacion_ordenada = poblacion_nueva_ordenada
        num_generaciones += 1
        print(f"Generación {num_generaciones} sin solución óptima.")
    
    print(f"\n No se encontró solución óptima en {max_generaciones} generaciones.")
    return mejor_solucion, mejor_fit



# Función que manda a llamar todo
def N_reinas(n, N, generaciones):
    
    poblacion_inicial = generar_poblacion_inicial(N, n)
    poblacion_ordenada = ordenar_poblacion(poblacion_inicial)
    tablero_solucion, fit_solucion = evolucionar(poblacion_ordenada, N, generaciones)

    if tablero_solucion is not None:
        print(f"\n Mejor solución encontrada: {tablero_solucion}")
        print(f"Valor de ajuste (fit) de la mejor solución: {fit_solucion}")
    else:
        print("No se encontró una solución dentro del límite de generaciones.")




n = 9 #Tamaño del tablero
N = 100 # Tamaño de la población
generaciones = 100000

N_reinas(n,N,generaciones)





