class Item_TMP:
    def __init__(self, price=None, name=None, type=None):
        self.price = price
        self.name = name
        self.count = 2
        self.type = type
        self.heal = 0

    @staticmethod
    def draw_item(screen, image, rect):
        screen.blit(image, rect)

    def use(self, player, index):
        item = list(player.items.values())[index]
        if item.count <= 0:
            return False, None 
        item.count -= 1
        return True, item
    
class Potion(Item_TMP):
    def __init__(self, price=2, name="Potion", type="heal"):
        super().__init__(price, name, type)
        self.heal = 30

class Hi_Potion(Item_TMP):
    def __init__(self, price=10, name="Hi-Potion", type="heal"):
        super().__init__(price, name, type)
        self.heal = 150

class X_Potion(Item_TMP):
    def __init__(self, price=25, name="X-Potion", type="heal"):
        super().__init__(price, name, type)
        self.heal = 500

class Battle_drum(Item_TMP):
    def __init__(self, price=20, name="Battle drum", type="misc"):
        super().__init__(price, name, type)

class Bomb(Item_TMP):
    def __init__(self, price=10, name="Bomb", type="misc"):
        super().__init__(price, name, type)

class Greed_bag(Item_TMP):
    def __init__(self, price=10, name="Bag of greed", type="misc"):
        super().__init__(price, name, type)

class Sword(Item_TMP):
    def __init__(self, price=50, name="Sword", type="weapon"):
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

class Hammer(Item_TMP):
    def __init__(self, price=50, name="Hammer", type="weapon"):
        super().__init__(price, name, type)
    
    def up_stats(self, player=None):
        self.save = (player.damage, player.max_health, player.evasion)
        player.damage *= 1.5
        player.evasion = 0
        player.max_health *= 2
        if player.health > player.max_health:
            player.health = player.max_health
        player.damage = round(player.damage, 0)
        player.health = round(player.health, 0)

    def return_stats(self, player):
        player.damage //= 1.5
        player.max_health //= 2
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