class Item_TMP:
    # Items = []
    def __init__(self, price, name):
        self.price = price
        self.name = name
        # Item_TMP.Items.append(self)
    
class Potion(Item_TMP):
    def __init__(self, price=5, name="Potion"):
        super().__init__(price, name)
        self.heal = 10

class Hi_Potion(Item_TMP):
    def __init__(self, price=20, name="Hi-potion"):
        super().__init__(price, name)
        self.heal = 100

class X_Potion(Item_TMP):
    def __init__(self, price=500, name="X-Potion"):
        super().__init__(price, name)
        self.heal = 500

class Battle_drum(Item_TMP):
    def __init__(self, price=500, name="Drum"):
        super().__init__(price, name)

    def up_stats(self, player=None):
        player.damage *= 2

class Bomb(Item_TMP):
    def __init__(self, price=300, name="Bomb"):
        super().__init__(price, name)
    
    def damage(self, monster=None):
        monster.health -= monster.health*0.5

class Greed_bag(Item_TMP):
    def __init__(self, price=50, name="Loot bag"):
        super().__init__(price, name)

class Longsword(Item_TMP):
    def __init__(self, price=500, name="Longsword"):
        super().__init__(price, name)

    def upstats(self, player=None):
        player.damage *= 1.3
        player.evasion += 0.1

class Mace(Item_TMP):
    def __init__(self, price=500, name="Mace"):
        super().__init__(price, name)
    
    def up_stats(self, player=None):
        player.damage *= 2
        player.evasion = 0

class Knife(Item_TMP):
    def __init__(self, price=500, name="Knife"):
        super().__init__(price, name)

    def up_stats(self, player=None):
        player.damage *= 0.5
        player.evasion += 0.5

# a = Potion()
# b = Hi_Potion()
# c = X_Potion()
# d = Battle_drum()
# e = Bomb()
# f = Greed_bag()
# g = Longsword()
# h = Mace()
# i = Knife()

# print(Item_TMP.Items)