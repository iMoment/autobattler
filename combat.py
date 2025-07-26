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
        dice_roll = self.roll_d20()
        adjusted_initiative = base_initiative + dice_roll
        return adjusted_initiative, dice_roll
    
    """Combat related methods"""
    # TODO: Can implement a hit_success RNG roll later; right now all attacks hit
    # Executes a single attack
    def perform_attack(self, attacker, defender):
        actual_damage = defender.take_damage(attacker.attack_dmg)

        log_entry = f"{attacker.name} attacks {defender.name}! Damage: {attacker.attack_dmg}, Defender defense: {defender.defense}, Actual damage: {actual_damage}"
        print(log_entry)
        self.combat_log.append(log_entry)

    # Executes one combat turn
    def execute_turn(self):
        self.turn_count += 1
        print(f"\n--- Turn {self.turn_count} ---")
        print(f"Player: {self.player}")
        print(f"Opponent: {self.opponent}")

        # 1. Determine initiative with d20 roll - See who acts 'first' in the round
        print("Determining initiative...")
        player_adjusted_initiative, player_dice_roll = self.roll_initiative(self.player.initiative)
        opponent_adjusted_initiative, opponent_dice_roll = self.roll_initiative(self.opponent.initiative)
        print(f"{self.player.name} rolled a {player_dice_roll}. Initiative score of {player_adjusted_initiative}.")
        print(f"{self.opponent.name} rolled a {opponent_dice_roll}. Initiative score of {opponent_adjusted_initiative}.")

        if self.player.is_alive and player_adjusted_initiative >= opponent_adjusted_initiative:
            self.perform_attack(self.player, self.opponent)
        elif self.opponent.is_alive and opponent_adjusted_initiative > player_adjusted_initiative:
            self.perform_attack(self.opponent, self.player)

    # Combat check to see if gamestate should continue
    def check_combat_status(self):
        if not self.player.is_alive and not self.opponent.is_alive:
            return CombatResult.DRAW
        elif not self.player.is_alive:
            return CombatResult.OPPONENT_VICTORY
        elif not self.opponent.is_alive:
            return CombatResult.PLAYER_VICTORY
        else:
            return CombatResult.CONTINUE

    # Main combat logic calculation
    def process_full_combat_with_results(self, max_turns=20):
        print(f"\n<=== LET THE BATTLE BEGIN! ===>")
        print(f"{self.player.name} vs {self.opponent.name}")

        while self.turn_count < max_turns:
            self.execute_turn()
            result = self.check_combat_status()

            if result != CombatResult.CONTINUE:
                print(f"\n<=== THE BATTLE HAS ENDED! ===>")
                print(f"Result: {result.value}")
                print(f"Turns taken: {self.turn_count}")
                return result
            
        # This handles the case when max turns have been reached
        print(f"\n<=== BATTLE TIMEOUT ===>")
        print(f"Combat ended due to turn limit; ya'll be weak af")
        return CombatResult.DRAW
    
    # Returns a summary of the combat
    def get_combat_summary(self):
        return {
            'turns': self.turn_count,
            'player_health': self.player.current_hp,
            'opponent_health': self.opponent.current_hp,
            'player_alive': self.player.is_alive,
            'opponent_alive': self.opponent.is_alive,
            'log': self.combat_log.copy()
        }
