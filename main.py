# Our autobattler project
from gamestate import GameState, GameStateManager
from combat import CombatResult, CombatManager
from character import Character

def main():
    # MAIN_GAME_LOOP
    print("Starting autobattler!")

    # TODO: Initialization, 2D list stage and movement not used yet
    game_state = GameStateManager(GameState.READY)

    # Add callback to monitor state changes
    game_state.add_state_change_callback(on_state_change)

    # Main game loop turn count limit
    # TODO: May be used to 'continue' string of battles with different opponents sequentially

    # Character Select
    # TODO: needs logic for player character class selection amongst available
    # hard-coded opponent for now, match-making selection with later implementation
    player, opponent = character_select_setup()

    while not game_state.is_terminated():
        print(f"Current state: {game_state.current_state.value}")

        if game_state.is_ready():
            handle_ready_state(game_state)
        elif game_state.is_battling():
            handle_battling_state(game_state, player, opponent)
        else:
            print(f"Unhandled state: {game_state.current_state}")
            break

    # MAIN_GAME_LOOP_HAS_ENDED
    if game_state.is_terminated():
        print("\n<=== GAME HAS BEEN TERMINATED ===>")

# Prompts user to select a given character
def character_select_setup():
    stanley = Character("Stanley", 100, 20, 5, 12)
    aaron = Character("Aaron", 140, 25, 10, 5)

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
            game_state.start_battle()
        elif action == 't':
            game_state.terminate()
        else:
            print(f"'{action}' is an invalid selection. Please select from the given options below: \n")

# Logic for handling the battling state, using combat manager
def handle_battling_state(game_state, player, opponent):
    print("Battle in progress...")

    # Initialize combat manager
    combat_manager = CombatManager(player, opponent)

    # Execute combat
    combat_result = combat_manager.process_full_combat_with_results()
    
    # Handle combat results and change game state if needed
    if combat_result == CombatResult.PLAYER_VICTORY:
        print(f"\nVictory! {player.name} defeated {opponent.name}!")
        # modifiers applied if additional game loops
        game_state.reset_to_ready()
    elif combat_result == CombatResult.OPPONENT_VICTORY:
        print(f"\n Defeat! {opponent.name} has defeated {player.name}!")
        print("Game Over Loser!")
        game_state.terminate()
    elif combat_result == CombatResult.DRAW:
        print(f"\n Draw! Both fighters are equally matched!")
        print("Game Over!")
        game_state.terminate()
    
    # Logic for printing combat summary
    combat_summary = combat_manager.get_combat_summary()
    print(f"\nCombat Summary:")
    print(f"- Turns: {combat_summary['turns']}")
    print(f"- {player.name}: {combat_summary['player_health']}/{player.max_hp} HP")
    print(f"- {opponent.name}: {combat_summary['opponent_health']}/{opponent.max_hp} HP")

# Callback function is called whenever game state changes
def on_state_change(previous_state, current_state):
    print(f"[STATE CHANGE] {previous_state.value if previous_state else 'None'} -> {current_state.value}")

if __name__ == "__main__":
    main()