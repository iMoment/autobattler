# Our project
import random

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
    # Create Battle Stage
    battle_stage = [None] * 12

    # Create two characters
    stanley = Character("Stanley", 100, 3, 10, 3, 10)
    aaron = Character("Aaron", 140, 2, 15, 2, 7)

    # Main game loop
    # Character Select
    print("Starting autobattler!")
    print("Choose 'Stanley' or 'Aaron' as your character.")
    character_select = input("Type 's' or 'a' to select. ")
    opponent = None
    if character_select == 's':
        character_select = stanley
        opponent = aaron
    else:
        character_select = aaron
        opponent = stanley

    print(f"You have selected {character_select.name}. Your opponent is {opponent.name}.\n")

    # Prepare battle stage with character
    #                          me                opp
    # |___| |___| |___| |___| |___| |___| |___| |___| |___| |___| |___| |___| 
    #   0     1.    2.    3.    4.    5.    6.    7.    8.    9.   10.   11

    battle_stage[4] = character_select
    battle_stage[7] = opponent

    ### Start Fight ###
    while True:
        # 1. Determine initiative - See who acts 'first' in the round
        print("Determining initiative...")
        character_d20_roll = random.randint(1, 20)
        opponent_d20_roll = random.randint(1, 20)
        character_adjusted_initiative = character_select.initiative + character_d20_roll
        opponent_adjusted_initiative = opponent.initiative + opponent_d20_roll
        print(f"{character_select.name} rolled a {character_d20_roll}. Initiative score of {character_adjusted_initiative}.")
        print(f"{opponent.name} rolled a {opponent_d20_roll}. Initiative score of {opponent_adjusted_initiative}.")

        # 2. Attack logic first, then incorporate movement
        # bug_fix: need to incorporate concurrency issue if initiative is tied
        if character_adjusted_initiative >= opponent_adjusted_initiative:
            print(f"{character_select.name} attacks first!")
            opponent.take_damage(character_select.name, character_select.attack_damage)
        if opponent_adjusted_initiative >= character_adjusted_initiative:
            print(f"{opponent.name} attacks first!")
            character_select.take_damage(opponent.name, opponent.attack_damage)


    






if __name__ == "__main__":
    main()
