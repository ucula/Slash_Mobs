class Item_TMP:
    # Items = []
    def __init__(self, price, name, type):
        self.price = price
        self.name = name

        self.type = type
        self.save = ()
    
    @staticmethod
    def draw_item(screen, image, x, y):
        screen.blit(image, (x, y))
    
class Potion(Item_TMP):
    def __init__(self, price=2, name="Potion", type="item"):
        super().__init__(price, name, type)
        self.heal = 10

class Hi_Potion(Item_TMP):
    def __init__(self, price=10, name="Hi-Potion", type="item"):
        super().__init__(price, name, type)
        self.heal = 100

class X_Potion(Item_TMP):
    def __init__(self, price=25, name="X-Potion", type="item"):
        super().__init__(price, name, type)
        self.heal = 500

class Battle_drum(Item_TMP):
    def __init__(self, price=4, name="Drum", type="item"):
        super().__init__(price, name, type)

    def up_stats(self, player=None):
        player.damage *= 2

class Bomb(Item_TMP):
    def __init__(self, price=8, name="Bomb", type="item"):
        super().__init__(price, name, type)
    
    def damage(self, monster=None):
        monster.health -= monster.health*0.5

class Greed_bag(Item_TMP):
    def __init__(self, price=8, name="Loot bag", type="item"):
        super().__init__(price, name, type)

class Longsword(Item_TMP):
    def __init__(self, price=50, name="Longsword", type="weapon"):
        super().__init__(price, name, type)

    def up_stats(self, player=None):
        player.damage *= 1.5
        player.damage = round(player.damage, 0)
        player.max_health *= 1.2
        if player.health > player.max_health:
            player.health = player.max_health
        player.damage = round(player.damage, 0)
        player.health = round(player.health, 0)
    
    def return_stats(self, player):
        player.damage //= 1.5
        player.max_health //= 1.2
        if player.health > player.max_health:
            player.health = player.max_health
        player.damage = round(player.damage, 0)
        player.health = round(player.health, 0)

class Mace(Item_TMP):
    def __init__(self, price=50, name="Mace", type="weapon"):
        super().__init__(price, name, type)
    
    def up_stats(self, player=None):
        self.save = (player.damage, player.max_health, player.evasion)
        player.damage *= 2.5
        player.evasion = 0
        player.max_health *= 3
        if player.health > player.max_health:
            player.health = player.max_health
        player.damage = round(player.damage, 0)
        player.health = round(player.health, 0)

    def return_stats(self, player):
        player.damage //= 2.5
        player.max_health //= 3
        player.evasion = 0.2
        if player.health > player.max_health:
            player.health = player.max_health
        player.damage = round(player.damage, 0)
        player.health = round(player.health, 0)

class Knife(Item_TMP):
    def __init__(self, price=50, name="Knife", type="weapon"):
        super().__init__(price, name, type)

    def up_stats(self, player=None):
        self.save = (player.damage, player.max_health, player.evasion)
        player.damage *= 0.7
        player.evasion += 0.6
        player.max_health *= 0.7
        if player.health > player.max_health:
            player.health = player.max_health
        player.damage = round(player.damage)
        player.health = round(player.health)

    def return_stats(self, player):
        player.damage //= 0.7
        player.max_health //= 0.7
        player.evasion -= 0.6
        if player.health > player.max_health:
            player.health = player.max_health
        player.damage = round(player.damage)
        player.health = round(player.health)