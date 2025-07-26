# Our project
import random
from gamestate import GameState, GameStateManager
from combat import CombatResult, CombatManager

def main():
    """Main Game Loop"""
    print("Starting autobattler!")

    # TODO: Initialization, 2D list stage and movement not used yet
    game_state = GameStateManager(GameState.READY)

    # Add callback to monitor state changes
    game_state.add_state_change_callback(on_state_change)

    # Character Select
    # TODO: needs logic for player character class selection amongst available
    # hard-coded opponent for now, match-making selection with later implementation
    player, opponent = character_select_setup()

    while not game_state.is_terminated():
        print(f"Current state: {game_state.current_state.value}")

        # TODO: Handle different game states
        if game_state.is_ready():
            handle_ready_state(game_state)
        elif game_state.is_battling():
            handle_battling_state(game_state, player, opponent)
        else:
            print(f"Unhandled state: {game_state.current_state}")
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
def handle_ready_state(game_state):
    while game_state.is_ready():
        # TODO: Any pre-battling calculations should be done here eventually (healing, leveling up, etc)

        action = input("Game is ready. Press 'b' to start battle, or 't' to terminate. ")
        if action == 'b':
            # Start battling
            game_state.start_battle()
        elif action == 't':
            # Terminate the game
            game_state.terminate()
        else:
            print(f"'{action}' is an invalid selection. Please select from the given options below: \n")

# Logic for handling the battling state, using combat manager
def handle_battling_state(game_state, player, opponent):
        print("Battle in progress...")

        # Initialize combat manager
        combat_manager = CombatManager(player, opponent)

        # 1. Determine initiative with d20 roll - See who acts 'first' in the round
        print("Determining initiative...")
        player_adjusted_initiative, player_dice_roll = combat_manager.roll_initiative(player.initiative)
        opponent_adjusted_initiative, opponent_dice_roll = combat_manager.roll_initiative(opponent.initiative)
        print(f"{player.name} rolled a {player_dice_roll}. Initiative score of {player_adjusted_initiative}.")
        print(f"{opponent.name} rolled a {opponent_dice_roll}. Initiative scorec of {opponent_adjusted_initiative}.")

        # 2. 
    
    
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

# Callback function is called whenever game state changes
def on_state_change(previous_state, current_state):
    print(f"[STATE CHANGE] {previous_state.value if previous_state else 'None'} -> {current_state.value}")





if __name__ == "__main__":
    main()
