# Character class which represents a single participant
# in our autobattler game

class Character:
    def __init__(self, name, max_hp=100, attack_dmg=10, defense=5, initiative=10):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack_dmg = attack_dmg
        self.defense = defense
        self.initiative = initiative
        self.is_alive = True

    # Returns actual damage value after defense stat applied
    def take_damage(self, damage):
        actual_damage = max(0, damage - self.defense)
        self.current_hp = max(0, self.current_hp - actual_damage)

        if self.current_hp <= 0:
            self.is_alive = False
            print(f"{self.name} has been defeated!")

        return actual_damage
    
    """Convenience Methods"""
    # Returns current_hp as a percentage
    def get_hp_percentage(self):
        return (self.current_hp / self.max_hp) * 100
    
    # Console output convenience
    def __str__(self):
        return f"{self.name}: {self.current_hp}/{self.max_hp} HP"