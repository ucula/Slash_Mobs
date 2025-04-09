from ui import AllUI

class Player:
    def __init__(self, name: str):
        self.ui = AllUI()
        self.name = name
        self.health = 100
        self.level = 1
        self.exp = 0
        self.damage = 1
        self.evasion = 0.1
        self.skill1_status = False
        self.skill2_status = False
    
    def level_up(self):
        self.level += 1
        self.damage += 0.5
        if self.level == 5:
            self.skill1_status = True
            print("Skill1 unlocked!")

        if self.level == 10:
            self.skill2_status = True
            print("Skill2 unlocked!")
        print("Level up!")

    def reduce_hp(self, damage: int):
        self.health -= damage
        if self.health <= 0:
            self.die()

    def die(self):
        self.ui.draw_game_over()

    def attack(self, enemy):
        pass

    def dodge(self):
        pass

    def escape(self):
        pass

    def buy(self, item_name: str):
        pass

    def sell(self, item_name: str):
        pass

    def discard_item(self, item_name: str):
        pass

    def skill1(self):
        pass

    def skill2(self):
        pass