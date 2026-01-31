"""
扩展示例 - 展示如何添加新功能
"""

from game import Item, Location, Enemy, Player


# ============ 新物品类型示例 ============

class MagicScroll(Item):
    """魔法卷轴 - 造成大量伤害"""
    
    def __init__(self):
        super().__init__("魔法卷轴", "释放强大的魔法攻击", "消耗品")
        self.damage = 50
    
    def use(self, player):
        # 需要在战斗中使用
        print(f"你使用了{self.name}！")
        print(f"（在战斗系统中会造成{self.damage}点伤害）")
        return True


class ArmorPiece(Item):
    """护甲 - 增加防御力"""
    
    def __init__(self, name, defense_bonus):
        super().__init__(name, f"增加{defense_bonus}点防御力", "装备")
        self.defense_bonus = defense_bonus
        self.equipped = False
    
    def use(self, player):
        if not self.equipped:
            player.defense += self.defense_bonus
            self.equipped = True
            print(f"你装备了{self.name}，防御力+{self.defense_bonus}")
            return False  # 不消耗物品
        else:
            print("已经装备了这件护甲！")
            return False


class KeyItem(Item):
    """钥匙类物品 - 用于解锁特定区域"""
    
    def __init__(self, name, unlocks):
        super().__init__(name, f"可以打开{unlocks}", "钥匙")
        self.unlocks = unlocks
    
    def use(self, player):
        print(f"这把钥匙需要在{self.unlocks}使用")
        return False


# ============ 特殊敌人类型示例 ============

class BossEnemy(Enemy):
    """Boss敌人 - 具有特殊技能"""
    
    def __init__(self, name, hp, attack, defense, exp_reward, gold_reward):
        super().__init__(name, hp, attack, defense, exp_reward, gold_reward)
        self.special_attack_cooldown = 0
    
    def special_attack(self):
        """特殊攻击 - 造成双倍伤害"""
        if self.special_attack_cooldown == 0:
            self.special_attack_cooldown = 3
            return self.attack * 2
        return None
    
    def update_cooldown(self):
        """更新冷却时间"""
        if self.special_attack_cooldown > 0:
            self.special_attack_cooldown -= 1


class HealingEnemy(Enemy):
    """会治疗的敌人"""
    
    def __init__(self, name, hp, attack, defense, exp_reward, gold_reward, heal_amount):
        super().__init__(name, hp, attack, defense, exp_reward, gold_reward)
        self.heal_amount = heal_amount
        self.heal_cooldown = 0
    
    def try_heal(self):
        """尝试治疗自己"""
        if self.heal_cooldown == 0 and self.hp < self.max_hp * 0.5:
            self.hp = min(self.max_hp, self.hp + self.heal_amount)
            self.heal_cooldown = 4
            return True
        
        if self.heal_cooldown > 0:
            self.heal_cooldown -= 1
        
        return False


# ============ 互动式地点示例 ============

class Shop(Location):
    """商店地点"""
    
    def __init__(self, name, description):
        super().__init__(name, description)
        self.shop_items = {
            "治疗药水": (20, HealingPotion),
            "铁剑": (50, lambda: Weapon("铁剑", "普通的铁剑", 5)),
            "皮甲": (40, lambda: ArmorPiece("皮甲", 3))
        }
    
    def show_shop(self, player):
        """显示商店商品"""
        print(f"\n欢迎来到{self.name}！")
        print("可购买的商品：")
        for item_name, (price, _) in self.shop_items.items():
            print(f"  - {item_name}: {price}金币")
        print(f"\n你的金币: {player.gold}")
    
    def buy_item(self, item_name, player):
        """购买物品"""
        if item_name in self.shop_items:
            price, item_creator = self.shop_items[item_name]
            
            if player.gold >= price:
                player.gold -= price
                item = item_creator() if callable(item_creator) else item_creator
                player.add_item(item)
                print(f"购买成功！获得了{item_name}")
                return True
            else:
                print("金币不足！")
                return False
        else:
            print(f"商店没有{item_name}")
            return False


class Puzzle(Location):
    """谜题地点 - 需要解谜才能通过"""
    
    def __init__(self, name, description, puzzle_text, correct_answer):
        super().__init__(name, description)
        self.puzzle_text = puzzle_text
        self.correct_answer = correct_answer
        self.solved = False
    
    def show_puzzle(self):
        """显示谜题"""
        if not self.solved:
            print(f"\n{self.puzzle_text}")
            return False
        else:
            print("谜题已解开！")
            return True
    
    def solve(self, answer):
        """尝试解谜"""
        if answer.lower() == self.correct_answer.lower():
            self.solved = True
            print("答案正确！谜题已解开！")
            return True
        else:
            print("答案错误...")
            return False


# ============ NPC系统示例 ============

class NPC:
    """非玩家角色"""
    
    def __init__(self, name, dialogue):
        self.name = name
        self.dialogue = dialogue
        self.quest = None
    
    def talk(self):
        """对话"""
        print(f"\n{self.name}: {self.dialogue}")
    
    def give_quest(self, quest):
        """给予任务"""
        self.quest = quest


class Quest:
    """任务系统"""
    
    def __init__(self, name, description, objective, reward_exp, reward_gold):
        self.name = name
        self.description = description
        self.objective = objective  # 例如: {"kill": {"野狼": 3}}
        self.reward_exp = reward_exp
        self.reward_gold = reward_gold
        self.completed = False
        self.progress = {}
    
    def update_progress(self, action_type, target):
        """更新任务进度"""
        if action_type in self.objective:
            if target in self.objective[action_type]:
                if target not in self.progress:
                    self.progress[target] = 0
                
                self.progress[target] += 1
                
                # 检查是否完成
                if self.progress[target] >= self.objective[action_type][target]:
                    return True
        
        return False
    
    def check_completion(self):
        """检查任务是否完成"""
        for action_type, targets in self.objective.items():
            for target, required in targets.items():
                if self.progress.get(target, 0) < required:
                    return False
        
        self.completed = True
        return True
    
    def show_progress(self):
        """显示任务进度"""
        print(f"\n任务: {self.name}")
        print(f"描述: {self.description}")
        print("进度:")
        
        for action_type, targets in self.objective.items():
            for target, required in targets.items():
                current = self.progress.get(target, 0)
                print(f"  - {target}: {current}/{required}")


# ============ 使用示例 ============

def example_usage():
    """展示如何使用扩展功能"""
    
    # 创建商店
    shop = Shop("冒险者商店", "一个销售各种冒险用品的商店")
    
    # 创建谜题地点
    puzzle_room = Puzzle(
        "密室",
        "一个神秘的房间，门上刻着古老的文字",
        "谜题：什么东西早上四条腿，中午两条腿，晚上三条腿？",
        "人"
    )
    
    # 创建NPC和任务
    village_elder = NPC("村长", "欢迎来到我们的村庄，勇敢的冒险者！")
    wolf_quest = Quest(
        "狼群威胁",
        "森林里的狼群威胁着村庄的安全",
        {"kill": {"野狼": 3}},
        100,
        50
    )
    village_elder.give_quest(wolf_quest)
    
    # 创建特殊敌人
    dragon_boss = BossEnemy("暗影龙", 200, 30, 15, 1000, 500)
    healer_enemy = HealingEnemy("治疗僧", 80, 12, 5, 150, 80, 30)
    
    # 创建特殊物品
    magic_scroll = MagicScroll()
    steel_armor = ArmorPiece("钢铁护甲", 10)
    boss_key = KeyItem("黄金钥匙", "最终BOSS的房间")
    
    print("扩展功能示例加载完成！")
    print("\n你可以将这些类和概念整合到主游戏中。")


if __name__ == "__main__":
    example_usage()
