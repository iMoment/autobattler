# Our project
import random
from gamestate import GameState, GameStateManager

class Character:
    def __init__(self, name, hit_points, movement_speed, attack_damage, attack_range, initiative):
        self.name = name
        self.hit_points = hit_points
        self.movement_speed = movement_speed
        self.attack_damage = attack_damage
        self.attack_range = attack_range
        self.initiative = initiative

    def take_damage(self, opponent_name, damage):
        print(f"{opponent_name} attacks for {damage} damage!")
        self.hit_points -= damage
        print(f"{self.name} has received {damage} damage.")
        self.print_status()

        if self.hit_points <= 0:
            raise Exception(f"{self.name} got owned! {self.name} has died.")
        
    def print_status(self):
        print(f"{self.name} has {self.hit_points} remaining.\n")


def main():
    """Main Game Loop"""
    print("Starting autobattler!")

    # TODO: Initialization, 2D list stage and movement not used yet
    game_state = GameStateManager(GameState.READY)

    # Character Select
    player, opponent = character_select_setup()

    while not game_state.is_terminated():
        print(f"Current state: {game_state.current_state.value}")

        # TODO: Handle different game states
        if game_state.is_ready():
            handle_ready_state(game_state, player, opponent)
        elif game_state.is_battling():
            pass
        else:
            print(f"This state is not handled: {game_state.current_state}")
            break

    """Main Game Loop Has Ended"""
    if game_state.is_terminated():
        print("Another one bites the dust...")

# Prompts user to select a given character
def character_select_setup():
    stanley = Character("Stanley", 100, 3, 10, 3, 10)
    aaron = Character("Aaron", 140, 2, 15, 2, 7)

    print("Choose 'Stanley' or 'Aaron' as your character.")
    character_select = input("Type 's' or 'a' to select. ")

    if character_select == 's':
        print(f"You have selected {stanley.name}. Your opponent is {aaron.name}.\n")
        return stanley, aaron
    else:
        print(f"You have selected {aaron.name}. Your opponent is {stanley.name}.\n")
        return aaron, stanley

# Logic for handling the ready state
def handle_ready_state(game_state, player, opponent):
    action = input("Game is ready. Press 'b' to start battle, or 't' to terminate.")
    if action == 'b':
        # 1. Determine initiative with d20 roll - See who acts 'first' in the round
        print("Determining initiative...")
        player_d20_roll = random.randint(1, 20)
        opponent_d20_roll = random.randint(1, 20)
        player_adjusted_initiative = player.initiative + player_d20_roll
        opponent_adjusted_initiative = opponent.initiative + opponent_d20_roll
        print(f"{player.name} rolled a {player_d20_roll}. Initiative score of {player_adjusted_initiative}.")
        print(f"{opponent.name} rolled a {opponent_d20_roll}. Initiative scorec of {opponent_adjusted_initiative}.")

        # 2. Start battling
        game_state.start_battle()
    elif action == 't':
        # 1. Terminate the game
        game_state.terminate()
    else:
        print("user has pressed a an invalid key")

# Logic for handling the battling state
def handle_battling_state(game_state):
    
    
    ### Start Fight ###
    # while True:

    #     # 2. Attack logic first, then incorporate movement
    #     # bug_fix: need to incorporate concurrency issue if initiative is tied
    #     if character_adjusted_initiative >= opponent_adjusted_initiative:
    #         print(f"{character_select.name} attacks first!")
    #         opponent.take_damage(character_select.name, character_select.attack_damage)
    #     if opponent_adjusted_initiative >= character_adjusted_initiative:
    #         print(f"{opponent.name} attacks first!")
    #         character_select.take_damage(opponent.name, opponent.attack_damage)





if __name__ == "__main__":
    main()
