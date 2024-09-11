#!/usr/bin/env python
# coding: utf-8

# Daniel Rojo Mata
# Inteligencia Artificial, Semestre 2025-I

# Algoritmo Recocido Simulado
# No se especifica un problema en particular,
# solo se da el algoritmo de manera general

import random
import math 

class Problem:
    def __init__(self, initial_state):
        self.initial_state = initial_state  # El estado inicial del problema

    def initial_state(self):
        """Devuelve el estado inicial."""
        return self.initial_state

    def successors(self, state):
        """Genera una lista de sucesores para el estado actual.
           Este método debe ser definido según el problema específico."""
        pass  # Implementa la generación de sucesores según tu problema

    def value(self, state):
        """Calcula el valor (o costo) del estado actual.
           Debe ser definido según el problema específico."""
        pass  # Implementa la función de evaluación para el estado


class Schedule:
    def __init__(self, T0, alpha):
        self.T0 = T0  # Temperatura inicial
        self.alpha = alpha  # Tasa de enfriamiento

    def __call__(self, t):
        """Devuelve la temperatura en el tiempo t."""
        return self.T0 * (self.alpha ** t)  # Ejemplo: enfriamiento exponencial



def simulated_annealing(problem, schedule, max_iterations=1000):
    current = problem.initial_state  # Estado inicial
    t = 1  # Iniciar el contador de tiempo

    while t <= max_iterations:  # Bucle con límite de iteraciones
        T = schedule(t)
        if T == 0:
            return current  # Devolver la mejor solución encontrada

        # Selecciona un sucesor aleatorio
        successors = problem.successors(current)
        next_state = random.choice(successors)

        E = problem.value(next_state) - problem.value(current)

        if E > 0:  # Si es mejor, lo acepta directamente
            current = next_state
        else:  # Si es peor, lo acepta con cierta probabilidad
            probability = math.exp(E / T)
            if random.random() < probability:
                current = next_state

        t += 1  # Incrementa el tiempo

    return current  # Devolver la mejor solución encontrada después de las iteraciones máximas

