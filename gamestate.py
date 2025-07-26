# This file holds the logic for our autobattler's game state
# The game state will be used for determining which calculations and actions
# can be performed, within the respective state

from enum import Enum

# Enum containing our game's possible game states
class GameState(Enum):
    READY = "ready"
    BATTLING = "battling"
    TERMINATED = "terminated"

# GameStateManager class that manages the current game state and state transitions
class GameStateManager:

    def __init__(self, initial_state=GameState.READY):
        self._current_state = initial_state
        self._previous_state = None
        self._state_change_callbacks = []

    # Returns the current game state
    @property
    def current_state(self):
        return self._current_state
    
    # Returns the previous game state
    @property
    def previous_state(self):
        return self._previous_state
    
    # Change to a new game state
    def set_state(self, new_state):
        if not isinstance(new_state, GameState):
            raise ValueError(f"Invalid state: {new_state}. Must be a GameState enum.")
        
        if new_state != self._current_state:
            self._previous_state = self._current_state
            self._current_state = new_state
            print(f"\nGame state has changed: {self._previous_state.value} -> {self._current_state.value}")

            # Notify any registered callbacks
            self._notify_state_change()

    """Convenience methods for setting state"""
    # Set game state to ready
    def reset_to_ready(self):
        self.set_state(GameState.READY)

    # Set game state to battling
    def start_battle(self):
        self.set_state(GameState.BATTLING)

    # Set game state to terminated
    def terminate(self):
        self.set_state(GameState.TERMINATED)

    """Game state value checks"""
    # Check if the game is in a ready state
    def is_ready(self):
        return self._current_state == GameState.READY
    
    # Check if the game is in a battling state
    def is_battling(self):
        return self._current_state == GameState.BATTLING
    
    # Check if the game is in a terminated state
    def is_terminated(self):
        return self._current_state == GameState.TERMINATED
    
    """Callback handlers on game state change if needed"""
    # Add a callback function to be called when state changes
    def add_state_change_callback(self, callback):
        self._state_change_callbacks.append(callback)
    
    # Notifies all registered callbacks of state change
    def _notify_state_change(self):
        for callback in self._state_change_callbacks:
            try:
                callback(self._previous_state, self._current_state)
            except Exception as e:
                print(f"Error in state change callback: {e}")
    
    # Console output convenience
    def __str__(self):
        return f"GameState: {self._current_state.value}"
    
    def __repr__(self):
        return f"GameStateManager(current_state={self._current_state})"