"""
玩家角色类
"""


class Player:
    """玩家角色"""
    
    def __init__(self, name):
        self.name = name
        self.level = 1
        self.exp = 0
        self.max_hp = 100
        self.hp = 100
        self.attack = 10
        self.defense = 5
        self.gold = 50
        self.inventory = []
        self.current_location = None
    
    def take_damage(self, damage):
        """受到伤害"""
        actual_damage = max(0, damage - self.defense)
        self.hp -= actual_damage
        return actual_damage
    
    def heal(self, amount):
        """恢复生命值"""
        self.hp = min(self.max_hp, self.hp + amount)
    
    def gain_exp(self, amount):
        """获得经验值"""
        self.exp += amount
        # 检查是否升级（每100经验升一级）
        while self.exp >= self.level * 100:
            self.level_up()
    
    def level_up(self):
        """升级"""
        self.level += 1
        self.max_hp += 20
        self.hp = self.max_hp
        self.attack += 5
        self.defense += 2
    
    def add_item(self, item):
        """添加物品到背包"""
        self.inventory.append(item)
    
    def remove_item(self, item_name):
        """从背包移除物品"""
        for item in self.inventory:
            if item.name == item_name:
                self.inventory.remove(item)
                return item
        return None
    
    def get_status_text(self):
        """获取角色状态文本"""
        return f"""{'='*40}
角色: {self.name}
等级: {self.level} | 经验值: {self.exp}/{self.level * 100}
生命值: {self.hp}/{self.max_hp}
攻击力: {self.attack} | 防御力: {self.defense}
金币: {self.gold}
{'='*40}"""
