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

    def __init__(self, player, opponent, play_space_size=12, player_start_pos=4, opponent_start_pos=7):
        self.player = player
        self.opponent = opponent
        self.play_space_size = play_space_size
        self.turn_count = 0
        self.combat_log = []

        # Sets the initial position of the two characters
        self.player.position = player_start_pos
        self.opponent.position = opponent_start_pos

        # Initialize the 2-D play space
        self.play_space = [None] * play_space_size
        self.update_play_space()
        

    # Updates the visual representation of the play space in the console
    def update_play_space(self):
        self.play_space = [' ___ '] * self.play_space_size
        self.play_space[self.player.position] = "You"
        self.play_space[self.opponent.position] = "Opp"

        # Handles displaying both characters in same location index
        if self.player.position == self.opponent.position:
            self.play_space[self.player.position] = "Both"

    # Renders the current play space onto the console
    def render_play_space(self):
        play_space_render = ''.join(self.play_space)
        positions = ''.join([str(i % 10) for i in range(self.play_space_size)])
        print(f"Field:     {play_space_render}")
        print(f"Positions: {positions}")
        print(f"You={self.player.name}(Pos:{self.player.position}), Opp={self.opponent.name}(Pos:{self.opponent.position})")

    # Moves a character randomly according to their movement speed
    def move_character(self, character):
        if not character.is_alive:
            return
        
        # -1 is left, 1 is right
        direction = random.choice([-1, 1])

        # New position calculation, do not allow exceeding of list boundary
        max_movement = min(character.movement_speed, self.play_space_size - 1)

        # Random movement distance (1 up to and including movement_speed)
        movement_distance = random.randint(1, max_movement)
        new_position = character.position + (direction * movement_distance)

        # Check for staying within list boundary
        new_position = max(0, min(self.play_space_size - 1, new_position))

        # Update positions
        old_position = character.position
        character.position = new_position

        # Logging of movement onto console
        direction_str = "left" if direction == -1 else "right"
        actual_distance = abs(new_position - old_position)

        movement_log = f"{character.name} moves {direction_str} {actual_distance} spaces (from {old_position} to {new_position})"
        print(movement_log)
        self.combat_log.append(movement_log)

    # Determines distance between two characters
    def determine_distance(self, character1, character2):
        return abs(character1.position - character2.position)
    
    # Check if target is within attack_range
    def is_within_attack_range(self, attacker, target):
        distance = self.determine_distance(attacker, target)
        return distance <= attacker.attack_range

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
    # Executes a single attack
    def perform_attack(self, attacker, defender):
        # Before any damage calcs, gotta check range
        if not self.is_within_attack_range(attacker, defender):
            distance = self.determine_distance(attacker, defender)
            log_entry = f"{attacker.name} cannot reach {defender.name}! Distance: {distance}, Range: {attacker.attack_range}"
            print(log_entry)
            self.combat_log.append(log_entry)
            return 0

        actual_damage = defender.take_damage(attacker.attack_dmg)

        log_entry = f"{attacker.name} attacks {defender.name}! Damage: {attacker.attack_dmg}, Defender defense: {defender.defense}, Actual damage: {actual_damage}"
        print(log_entry)
        self.combat_log.append(log_entry)

    # Executes one combat turn
    def execute_turn(self):
        self.turn_count += 1
        print(f"\n--- Turn {self.turn_count} ---")

        # Display play space at start of each turn
        self.render_play_space()
        print(f"Player: {self.player}")
        print(f"Opponent: {self.opponent}")

        # Movement phase, both characters will move
        print("\n<=== MOVEMENT PHASE ===>")
        if self.player.is_alive:
            self.move_character(self.player)
        if self.opponent.is_alive:
            self.move_character(self.opponent)

        # Update play space render after this movement
        self.update_play_space()
        print("\nAfter movement:")
        self.render_play_space()

        # Combat Phase, determine initiative with d20 roll - See who acts 'first' in the round
        print("\n<=== COMBAT PHASE ===>")
        print("Determining initiative...")
        player_adjusted_initiative, player_dice_roll = self.roll_initiative(self.player.initiative)
        opponent_adjusted_initiative, opponent_dice_roll = self.roll_initiative(self.opponent.initiative)
        print(f"{self.player.name} rolled a {player_dice_roll}. Initiative score of {player_adjusted_initiative}.")
        print(f"{self.opponent.name} rolled a {opponent_dice_roll}. Initiative score of {opponent_adjusted_initiative}.")

        if self.player.is_alive and player_adjusted_initiative >= opponent_adjusted_initiative:
            self.perform_attack(self.player, self.opponent)
        elif self.opponent.is_alive and opponent_adjusted_initiative > player_adjusted_initiative:
            self.perform_attack(self.opponent, self.player)

        # Update play space render after combat occurs
        self.update_play_space()

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
            'player_final_pos': self.player.position,
            'opponent_final_pos': self.opponent.position,
            'distance': self.determine_distance(self.player, self.opponent),
            'log': self.combat_log.copy()
        }
