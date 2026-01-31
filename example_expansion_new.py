"""
扩展示例 - 使用新模块化结构
展示如何基于新架构添加新功能
"""

from src.models import Item, Location, Enemy, Player, HealingPotion, Weapon


# ============ 新物品类型示例 ============

class MagicScroll(Item):
    """魔法卷轴 - 造成大量伤害"""
    
    def __init__(self):
        super().__init__("魔法卷轴", "释放强大的魔法攻击", "消耗品")
        self.damage = 50
    
    def use(self, player):
        # 在战斗中使用会造成伤害
        return (f"你使用了{self.name}！造成了{self.damage}点魔法伤害！", True)


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
            return (f"你装备了{self.name}，防御力+{self.defense_bonus}", False)
        else:
            return ("已经装备了这件护甲！", False)


class KeyItem(Item):
    """钥匙类物品 - 用于解锁特定区域"""
    
    def __init__(self, name, unlocks):
        super().__init__(name, f"可以打开{unlocks}", "钥匙")
        self.unlocks = unlocks
    
    def use(self, player):
        return (f"这把钥匙需要在{self.unlocks}使用", False)


# ============ 特殊敌人类型示例 ============

class BossEnemy(Enemy):
    """Boss敌人 - 具有特殊技能"""
    
    def __init__(self, name, hp, attack, defense, exp_reward, gold_reward):
        super().__init__(name, hp, attack, defense, exp_reward, gold_reward)
        self.special_attack_cooldown = 0
        self.is_boss = True
    
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
    
    def __init__(self, name, hp, attack, defense, exp_reward, gold_reward, heal_amount=20):
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
            "皮甲": (40, lambda: ArmorPiece("皮甲", 3)),
            "魔法卷轴": (80, MagicScroll)
        }
    
    def get_shop_inventory(self):
        """获取商店库存列表"""
        return [(name, price) for name, (price, _) in self.shop_items.items()]
    
    def buy_item(self, item_name, player):
        """购买物品"""
        if item_name in self.shop_items:
            price, item_creator = self.shop_items[item_name]
            
            if player.gold >= price:
                player.gold -= price
                item = item_creator() if callable(item_creator) else item_creator
                player.add_item(item)
                return (True, f"购买成功！获得了{item_name}")
            else:
                return (False, "金币不足！")
        else:
            return (False, f"商店没有{item_name}")


class Puzzle(Location):
    """谜题地点 - 需要解谜才能通过"""
    
    def __init__(self, name, description, puzzle_text, correct_answer):
        super().__init__(name, description)
        self.puzzle_text = puzzle_text
        self.correct_answer = correct_answer.lower()
        self.solved = False
    
    def check_answer(self, answer):
        """检查答案是否正确"""
        if answer.lower() == self.correct_answer:
            self.solved = True
            return (True, "答案正确！谜题已解开！")
        else:
            return (False, "答案错误...")


# ============ NPC系统示例 ============

class NPC:
    """非玩家角色"""
    
    def __init__(self, name, dialogue):
        self.name = name
        self.dialogue = dialogue
        self.quests = []
    
    def add_quest(self, quest):
        """添加任务"""
        self.quests.append(quest)
    
    def get_available_quests(self):
        """获取可用任务"""
        return [q for q in self.quests if not q.accepted and not q.completed]


class Quest:
    """任务系统"""
    
    def __init__(self, name, description, objective, reward_exp, reward_gold):
        self.name = name
        self.description = description
        self.objective = objective  # 例如: {"kill": {"野狼": 3}}
        self.reward_exp = reward_exp
        self.reward_gold = reward_gold
        self.accepted = False
        self.completed = False
        self.progress = {}
    
    def accept(self):
        """接受任务"""
        self.accepted = True
    
    def update_progress(self, action_type, target):
        """更新任务进度"""
        if not self.accepted or self.completed:
            return False
        
        if action_type in self.objective:
            if target in self.objective[action_type]:
                if target not in self.progress:
                    self.progress[target] = 0
                
                self.progress[target] += 1
                
                # 检查是否完成
                if self.check_completion():
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
    
    def get_progress_text(self):
        """获取任务进度文本"""
        lines = [f"任务: {self.name}", f"描述: {self.description}", "进度:"]
        
        for action_type, targets in self.objective.items():
            for target, required in targets.items():
                current = self.progress.get(target, 0)
                lines.append(f"  - {target}: {current}/{required}")
        
        return "\n".join(lines)


# ============ 示例：如何创建扩展内容 ============

def create_expansion_content():
    """创建扩展内容示例"""
    
    # 创建商店
    shop = Shop("冒险者商店", "一个销售各种冒险用品的商店。")
    
    # 创建谜题
    puzzle_room = Puzzle(
        "密室",
        "一个神秘的房间，门上刻着古老的文字。",
        "谜题：什么东西早上四条腿，中午两条腿，晚上三条腿？",
        "人"
    )
    
    # 创建NPC
    village_elder = NPC("村长", "欢迎来到我们的村庄，勇敢的冒险者！")
    
    # 创建任务
    wolf_quest = Quest(
        "狼群威胁",
        "森林里的狼群威胁着村庄的安全，击败3只野狼",
        {"kill": {"野狼": 3}},
        100,
        50
    )
    village_elder.add_quest(wolf_quest)
    
    # 创建特殊敌人
    dragon_boss = BossEnemy("暗影龙", 200, 30, 15, 1000, 500)
    healer_enemy = HealingEnemy("治疗僧", 80, 12, 5, 150, 80)
    
    # 创建特殊物品
    magic_scroll = MagicScroll()
    steel_armor = ArmorPiece("钢铁护甲", 10)
    boss_key = KeyItem("黄金钥匙", "最终BOSS的房间")
    
    return {
        'locations': [shop, puzzle_room],
        'npcs': [village_elder],
        'enemies': [dragon_boss, healer_enemy],
        'items': [magic_scroll, steel_armor, boss_key]
    }


if __name__ == "__main__":
    print("扩展内容示例（基于新模块化结构）")
    print("="*50)
    content = create_expansion_content()
    print(f"✓ 创建了 {len(content['locations'])} 个新地点")
    print(f"✓ 创建了 {len(content['npcs'])} 个NPC")
    print(f"✓ 创建了 {len(content['enemies'])} 个特殊敌人")
    print(f"✓ 创建了 {len(content['items'])} 个特殊物品")
    print("\n你可以将这些内容整合到游戏引擎中！")
