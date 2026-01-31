"""
物品类
"""


class Item:
    """物品基类"""
    
    def __init__(self, name, description, item_type="其他"):
        self.name = name
        self.description = description
        self.item_type = item_type
    
    def use(self, player):
        """使用物品"""
        return f"你使用了 {self.name}"


class HealingPotion(Item):
    """治疗药水"""
    
    def __init__(self, heal_amount=30):
        super().__init__("治疗药水", "恢复30点生命值", "消耗品")
        self.heal_amount = heal_amount
    
    def use(self, player):
        if player.hp >= player.max_hp:
            return ("你的生命值已满，无需使用药水！", False)
        
        player.heal(self.heal_amount)
        return (f"你使用了治疗药水，恢复了 {self.heal_amount} 点生命值\n当前生命值: {player.hp}/{player.max_hp}", True)


class Weapon(Item):
    """武器"""
    
    def __init__(self, name, description, attack_bonus):
        super().__init__(name, description, "武器")
        self.attack_bonus = attack_bonus
