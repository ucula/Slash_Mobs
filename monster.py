import random

class Monsters:
    monster_data = {}

    @classmethod
    def display_monster(cls):
        string = []
        for i, (key, value) in enumerate(cls.monster_data.items()):
            string.append(f"{i+1}. {key} with {value.health} hp and {value.damage} damage")

        return "\n".join(string)
        
class Create_Monster:
    def __init__(self, name, health=100, damage=1, evasion=0.1):
        self.name = name
        self.health = health
        self.damage = damage
        self.level = 1
        self.evasion = evasion
    
    def reduce_hp(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        pass

    def attack(self):
        pass

    def dodge(self):
        pass
    
class Slime(Monsters):
    def __init__(self):
        super().__init__(name="Slime", health=3, evasion=0)
        Monsters.monster_data[self.name] = self
    
class Goblin(Monsters):
    def __init__(self):
        super().__init__(name="Goblin", health=10, evasion=0.1)
        self.hunter_instinct_rate = 0.14
        Monsters.monster_data[self.name] = self
    
    def hunter_instinct(self):
        self.damage *= 1.2

class Hop_Goblin(Goblin):
    def __init__(self):
        super().__init__(name="Hop Goblin", health=20, evasion=0.15)
        self.potion_rate = 0.15

    def potion(self):
        if self.health == 20:
            random.choice[self.attack(), self.hunter_instinct()]
        else:
            self.health += 5
