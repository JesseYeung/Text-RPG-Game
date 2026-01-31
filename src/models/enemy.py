"""
敌人类
"""


class Enemy:
    """敌人"""
    
    def __init__(self, name, hp, attack, defense, exp_reward, gold_reward):
        self.name = name
        self.max_hp = hp
        self.hp = hp
        self.attack = attack
        self.defense = defense
        self.exp_reward = exp_reward
        self.gold_reward = gold_reward
    
    def take_damage(self, damage):
        """受到伤害"""
        actual_damage = max(0, damage - self.defense)
        self.hp -= actual_damage
        return actual_damage
    
    def is_alive(self):
        """是否存活"""
        return self.hp > 0
