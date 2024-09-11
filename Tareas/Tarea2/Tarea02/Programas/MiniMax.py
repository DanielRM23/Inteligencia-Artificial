#!/usr/bin/env python
# coding: utf-8

# Daniel Rojo Mata
# Inteligencia Artificial, Semestre 2025-I

# Algoritmo MiniMax
# No se especifica un problema en particular,
# solo se da el algoritmo de manera general


# Implementación de Minimax en Python
class Game:
    """
    Clase general que define un juego de dos jugadores para el algoritmo Minimax.
    """
    
    def __init__(self, initial_state):
        """
        Inicializa el juego con el estado inicial.
        initial_state: Representa el estado inicial del juego.
        """
        self.initial_state = initial_state

    def to_move(self, state):
        """
        Devuelve el jugador que tiene el turno en el estado actual.
        Debe ser implementado por el juego específico.
        """
        pass 
    
    def actions(self, state):
        """
        Devuelve una lista de acciones legales en el estado actual.
        Debe ser implementado por el juego específico.
        """
        pass

    def result(self, state, action):
        """
        Devuelve el estado resultante después de aplicar una acción.
        Debe ser implementado por el juego específico.
        """
        pass

    def is_terminal(self, state):
        """
        Devuelve True si el estado es terminal (el juego ha terminado).
        Debe ser implementado por el juego específico.
        """
        pass

    def utility(self, state, player):
        """
        Devuelve el valor de utilidad del estado para el jugador dado.
        Debe ser implementado por el juego específico.
        """
        pass



def minimax_search(game, state):
    """
    Función principal de búsqueda Minimax.
    game: instancia del juego que tiene las funciones necesarias.
    state: el estado actual del juego.
    
    Retorna la mejor acción a tomar según el algoritmo Minimax.
    """
    player = game.to_move(state)  # Identifica quién es el jugador a mover
    value, move = max_value(game, state)  # Obtiene el valor máximo y el movimiento asociado
    return move  # Retorna el mejor movimiento encontrado


def max_value(game, state):
    """
    Función para calcular el valor máximo (jugador maximizador).
    game: instancia del juego.
    state: el estado actual del juego.
    
    Retorna una tupla (utilidad, movimiento) donde 'utilidad' es el valor máximo
    y 'movimiento' es la acción que produce ese valor.
    """
    if game.is_terminal(state):
        return game.utility(state, game.to_move(state)), None  # Si el estado es terminal, retorna la utilidad y ningún movimiento
    
    v = float('-inf')  # Inicializamos el valor máximo como menos infinito
    best_move = None
    
    # Itera sobre todas las acciones posibles en el estado actual
    for a in game.actions(state):
        v2, a2 = min_value(game, game.result(state, a))  # Llama a min_value para el valor del oponente
        if v2 > v:
            v, best_move = v2, a  # Actualiza el valor máximo y la mejor acción
    
    return v, best_move  # Retorna el mejor valor y la acción asociada


def min_value(game, state):
    """
    Función para calcular el valor mínimo (jugador minimizador).
    game: instancia del juego.
    state: el estado actual del juego.
    
    Retorna una tupla (utilidad, movimiento) donde 'utilidad' es el valor mínimo
    y 'movimiento' es la acción que produce ese valor.
    """
    if game.is_terminal(state):
        return game.utility(state, game.to_move(state)), None  # Si el estado es terminal, retorna la utilidad y ningún movimiento
    
    v = float('inf')  # Inicializamos el valor mínimo como infinito
    best_move = None
    
    # Itera sobre todas las acciones posibles en el estado actual
    for a in game.actions(state):
        v2, a2 = max_value(game, game.result(state, a))  # Llama a max_value para el valor del oponente
        if v2 < v:
            v, best_move = v2, a  # Actualiza el valor mínimo y la mejor acción
    
    return v, best_move  # Retorna el mejor valor y la acción asociada
