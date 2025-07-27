# Character class which represents a single participant
# in our autobattler game

class Character:
    def __init__(self, name, max_hp=100, attack_dmg=10, defense=5, movement_speed=2, attack_range=1, initiative=10):
        self.name = name
        self.max_hp = max_hp
        self.current_hp = max_hp
        self.attack_dmg = attack_dmg
        self.defense = defense
        self.initiative = initiative
        self.movement_speed = movement_speed
        self.attack_range = attack_range
        self.position = 0
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
    
# Tank Subclass
# Should focus on high health and defense, low values for movement and range
class Tank(Character):
    def __init__(self, name="Tank"):
        super().__init__(
            name = name,
            max_hp = 150,
            attack_dmg = 15,
            defense = 12,
            movement_speed = 1,
            attack_range = 1,
            initiative = 8,
        )

    @classmethod
    def description(cls):
        return "An absolute beast that can absorb hits, but moves like your standard Richmond local."
    
# Assassin Subclass
# Should focus on high movement and attack, low values for health and defense
class Assassin(Character):
    def __init__(self, name="Assasssin"):
        super().__init__(
            name = name,
            max_hp = 70,
            attack_dmg = 25,
            defense = 3,
            movement_speed = 4,
            attack_range = 1,
            initiative = 12,
        )
    
    @classmethod
    def description(cls):
        return "A nimble but power fighter, that's faster than how long I last in the bedroom."
    
# Warrior Subclass
# Should be balanced relative to the other two subclasses above
class Warrior(Character):
    def __init__(self, name="Warrior"):
        super().__init__(
            name = name,
            max_hp = 100,
            attack_dmg = 18,
            defense = 8,
            movement_speed = 3,
            attack_range = 2,
            initiative = 10,
        )
    
    @classmethod
    def description(cls):
        return "A nimble but power fighter, that's faster than how long I last in the bedroom."