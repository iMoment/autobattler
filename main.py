# Our autobattler project
import random
from gamestate import GameState, GameStateManager
from combat import CombatResult, CombatManager
from character import Character, Tank, Assassin, Warrior
from score import Score

def main():
    # MAIN_GAME_LOOP
    print("Starting autobattler!")

    display_character_classes()
    character_class = get_user_class_selection()
    player, opponent = create_characters(character_class)

    game_state = GameStateManager(GameState.READY)
    game_state.add_state_change_callback(on_state_change)
    score = Score()

    # Main game loop turn count limit
    # TODO: May be used to 'continue' string of battles with different opponents sequentially

    while not game_state.is_terminated():
        print(f"Current state: {game_state.current_state.value}")

        if game_state.is_ready():
            handle_ready_state(game_state)
        elif game_state.is_battling():
            handle_battling_state(game_state, player, opponent, score)
        else:
            print(f"Unhandled state: {game_state.current_state}")
            break

    # MAIN_GAME_LOOP_HAS_ENDED
    if game_state.is_terminated():
        print(f"\n<=== GAME HAS BEEN TERMINATED ===>")

# Convenience function for getting available character classes
def get_character_classes():
    return {
        "Tank": Tank,
        "Assassin": Assassin,
        "Warrior": Warrior,
    }

# Displays in the console available character classes a user can select to represent themselves
def display_character_classes():
    print("\n<=== CHARACTER CLASS SELECTION ===>")
    print("Choose your character class:\n")

    classes = get_character_classes()

    for index, (key, class_type) in enumerate(classes.items(), 1):
        # Need temp instance for displaying stats
        temp = class_type()

        print(f"{index}. {key}")
        print(f"   {class_type.description()}")
        print(f"   Health: {temp.max_hp}, Attack: {temp.attack_dmg}, Defense: {temp.defense}")
        print(f"   Movement: {temp.movement_speed}, Range: {temp.attack_range}\n")

# Get the user's character class selection
def get_user_class_selection():
    classes = get_character_classes()
    class_list = list(classes.keys())

    # Main selection loop
    while True:
        try:
            user_selection = input("Enter your selection (1-3): ").strip()
            selected = int(user_selection)

            if 1 <= selected <= len(class_list):
                selected_class_key = class_list[selected - 1]
                selected_class = classes[selected_class_key]
                print(f"\nYou have selected: {selected_class_key}")
                return selected_class
            else:
                print(f"Please enter a valid selection number.")
        except ValueError:
            print("Please enter a valid selection number.")

# Creates an instance of a character class
def create_characters(character_class):
    if character_class is None:
        return None
    
    available_classes = [Tank, Assassin, Warrior]
    player_character = character_class()
    available_classes.remove(character_class)
    opponent_character = random.choice(available_classes)()
    
    print(f"Character created: {player_character}")
    print(f"Your opponent is a/an: {opponent_character}\n")
        
    return player_character, opponent_character

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
def handle_battling_state(game_state, player, opponent, score):
    print("Battle in progress...")

    # Initialize combat manager
    combat_manager = CombatManager(player, opponent)

    # Execute combat
    combat_result = combat_manager.process_full_combat_with_results()
    
    # Handle combat results and change game state if needed
    if combat_result == CombatResult.PLAYER_VICTORY:
        print(f"\nVictory! {player.name} defeated {opponent.name}!")
        print(f"{score.increase_player_score()}\n{score.get_score()}")
        # modifiers applied if additional game loops
        game_state.reset_to_ready()
    elif combat_result == CombatResult.OPPONENT_VICTORY:
        print(f"\nDefeat! {opponent.name} has defeated {player.name}!")
        print(f"{score.increase_computer_score()} \n{score.get_score()}")
        print("Game Over Loser!")
        game_state.terminate()
    elif combat_result == CombatResult.DRAW:
        print(f"\nDraw! Both fighters are equally matched!")
        print(f"{score.get_score()}")
        print("Game Over!")
        game_state.terminate()
    
    # Logic for printing combat summary
    combat_summary = combat_manager.get_combat_summary()
    print(f"\nCombat Summary:")
    print(f"- Turns: {combat_summary['turns']}")
    print(f"- {player.name}: {combat_summary['player_health']}/{player.max_hp} HP (Final position: {combat_summary['player_final_pos']})")
    print(f"- {opponent.name}: {combat_summary['opponent_health']}/{opponent.max_hp} HP (Final position: {combat_summary['opponent_final_pos']})")
    print(f"- Final distance between characters: {combat_summary['distance']}\n")

# Callback function is called whenever game state changes
def on_state_change(previous_state, current_state):
    print(f"[STATE CHANGE] {previous_state.value if previous_state else 'None'} -> {current_state.value}")

if __name__ == "__main__":
    main()
    