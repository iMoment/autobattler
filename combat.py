# This file holds logic of our autobattler's combat system
# The combat system will be used for RNG dice rolling, combat mechanics and logging, and
# should integrate with our gamestate system

import random
from enum import Enum

# Enum containing the possible states of combat or 'battling'
class CombatResult(Enum):
    CONTINUE = "continue"
    PLAYER_VICTORY = "player_victory"
    OPPONENT_VICTORY = "opponent_victory"
    DRAW = "draw"

# This class should handle all combat logic, including dice rolling mechanics
class CombatManager:

    def __init__(self, player, opponent):
        self.player = player
        self.opponent = opponent
        self.turn_count = 0
        self.round_count = 0
        self.combat_log = []

    """Dice roll convenience methods"""
    # Returns a 20-sided die roll (1-20)
    def roll_d20(self):
        return random.randint(1, 20)
    
    # Returns normal die roll, unless number of sides is specified
    # May need this for special combat use cases
    def roll_dice(self, sides=6):
        return random.randint(1, sides)
    
    # Returns adjusted initiative value after d20 is applied, and d20 value
    def roll_initiative(self, base_initiative):
        dice_roll = self.roll_d20
        adjusted_initiative = base_initiative + dice_roll
        return adjusted_initiative, dice_roll
    
    """Combat related methods"""
    # Executes one combat turn
    def execute_turn(self):
        self.turn_count += 1
        print(f"\n--- Turn {self.turn_count} ---")
        print(f"Player: {self.player}")
        print(f"Opponent: {self.opponent}")

        

    # Main combat logic calculation
    def process_full_combat_with_results(self, max_turns=20):
        print(f"\n<=== LET THE BATTLE BEGIN! ===>")
        print(f"{self.player.name} vs {self.enemy.name}")

        while self.turn_count < max_turns:

