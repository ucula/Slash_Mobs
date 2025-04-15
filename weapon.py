class Weapons:
    weapon_data = {}

    @classmethod
    def display_weapon(cls):
        string = []
        for i, (key, value) in enumerate(cls.weapon_data.items()):
            string.append(f"{i+1}. {key} for {value.price} coins")

        return "\n".join(string)

class Create_Weapon:
    def __init__(self, name, price, damage, durability):
        self.name = name
        self.price = price
        self.damage = damage
        self.durability = durability
        Weapons.weapon_data[self.name] = self

    def __repr__(self):
        return f"Price = {self.price}, Damage = {self.damage}"
