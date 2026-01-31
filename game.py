#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文字角色扮演冒险游戏
一个简单但完整的文字RPG游戏模版
"""

import random
import sys


class Player:
    """玩家角色类"""
    
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
        print(f"\n🎉 恭喜！你升到了 {self.level} 级！")
        print(f"   生命值上限: {self.max_hp}")
        print(f"   攻击力: {self.attack}")
        print(f"   防御力: {self.defense}")
    
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
    
    def show_status(self):
        """显示角色状态"""
        print(f"\n{'='*50}")
        print(f"角色: {self.name}")
        print(f"等级: {self.level} | 经验值: {self.exp}/{self.level * 100}")
        print(f"生命值: {self.hp}/{self.max_hp}")
        print(f"攻击力: {self.attack} | 防御力: {self.defense}")
        print(f"金币: {self.gold}")
        print(f"{'='*50}\n")


class Item:
    """物品类"""
    
    def __init__(self, name, description, item_type="其他"):
        self.name = name
        self.description = description
        self.item_type = item_type
    
    def use(self, player):
        """使用物品"""
        print(f"你使用了 {self.name}")


class HealingPotion(Item):
    """治疗药水"""
    
    def __init__(self, heal_amount=30):
        super().__init__("治疗药水", "恢复30点生命值", "消耗品")
        self.heal_amount = heal_amount
    
    def use(self, player):
        if player.hp >= player.max_hp:
            print("你的生命值已满，无需使用药水！")
            return False
        
        player.heal(self.heal_amount)
        print(f"你使用了治疗药水，恢复了 {self.heal_amount} 点生命值")
        print(f"当前生命值: {player.hp}/{player.max_hp}")
        return True


class Weapon(Item):
    """武器"""
    
    def __init__(self, name, description, attack_bonus):
        super().__init__(name, description, "武器")
        self.attack_bonus = attack_bonus


class Enemy:
    """敌人类"""
    
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


class Location:
    """地点类"""
    
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.connections = {}  # 连接到其他地点 {方向: 地点对象}
        self.items = []
        self.enemies = []
        self.visited = False
    
    def add_connection(self, direction, location):
        """添加连接"""
        self.connections[direction] = location
    
    def describe(self):
        """描述地点"""
        print(f"\n📍 {self.name}")
        print(f"{self.description}")
        
        if self.items:
            print(f"\n你看到了: {', '.join([item.name for item in self.items])}")
        
        if self.enemies:
            print(f"\n⚠️  这里有敌人: {', '.join([enemy.name for enemy in self.enemies])}")
        
        if self.connections:
            print(f"\n可前往: {', '.join(self.connections.keys())}")


class Game:
    """游戏主类"""
    
    def __init__(self):
        self.player = None
        self.locations = {}
        self.current_location = None
        self.game_over = False
        
    def setup_game(self):
        """初始化游戏世界"""
        # 创建地点
        village = Location("新手村", "一个宁静的小村庄，这里是你冒险的起点。")
        forest = Location("迷雾森林", "茂密的森林，树木遮天蔽日，不时传来奇怪的声音。")
        cave = Location("黑暗洞穴", "阴暗潮湿的洞穴，深处似乎隐藏着什么。")
        ruins = Location("古老遗迹", "年代久远的遗迹，散发着神秘的气息。")
        mountain = Location("雪山顶峰", "白雪皑皑的山峰，这里是最终的挑战之地。")
        
        # 连接地点
        village.add_connection("北", forest)
        forest.add_connection("南", village)
        forest.add_connection("东", cave)
        forest.add_connection("西", ruins)
        cave.add_connection("西", forest)
        cave.add_connection("北", mountain)
        ruins.add_connection("东", forest)
        mountain.add_connection("南", cave)
        
        # 添加物品
        village.items.append(HealingPotion())
        forest.items.append(Weapon("铁剑", "一把普通的铁剑", 5))
        cave.items.append(HealingPotion())
        
        # 添加敌人
        forest.enemies.append(Enemy("野狼", 30, 8, 2, 50, 20))
        cave.enemies.append(Enemy("蝙蝠", 20, 6, 1, 30, 15))
        cave.enemies.append(Enemy("洞穴巨魔", 60, 15, 5, 100, 50))
        ruins.enemies.append(Enemy("骷髅战士", 40, 10, 3, 70, 30))
        mountain.enemies.append(Enemy("冰霜巨龙", 150, 25, 10, 500, 200))
        
        # 保存地点
        self.locations = {
            "新手村": village,
            "迷雾森林": forest,
            "黑暗洞穴": cave,
            "古老遗迹": ruins,
            "雪山顶峰": mountain
        }
        
        self.current_location = village
    
    def create_character(self):
        """创建角色"""
        print("\n" + "="*50)
        print("欢迎来到文字冒险世界！")
        print("="*50)
        
        name = input("\n请输入你的角色名字: ").strip()
        if not name:
            name = "冒险者"
        
        self.player = Player(name)
        self.player.current_location = self.current_location
        
        print(f"\n欢迎你，{name}！")
        print("你的冒险即将开始...")
        self.player.show_status()
    
    def show_help(self):
        """显示帮助信息"""
        print("\n" + "="*50)
        print("游戏指令:")
        print("  look/观察    - 查看当前位置")
        print("  go/前往 <方向> - 前往指定方向（北/南/东/西）")
        print("  status/状态  - 查看角色状态")
        print("  inventory/背包 - 查看背包")
        print("  take/拾取 <物品> - 拾取物品")
        print("  use/使用 <物品> - 使用物品")
        print("  attack/攻击 <敌人> - 攻击敌人")
        print("  help/帮助    - 显示帮助信息")
        print("  quit/退出    - 退出游戏")
        print("="*50 + "\n")
    
    def process_command(self, command):
        """处理玩家命令"""
        command = command.strip().lower()
        parts = command.split(maxsplit=1)
        
        if not parts:
            return
        
        action = parts[0]
        target = parts[1] if len(parts) > 1 else None
        
        if action in ["look", "观察", "l"]:
            self.current_location.describe()
        
        elif action in ["go", "前往", "走", "move"]:
            if not target:
                print("请指定方向（北/南/东/西）")
                return
            self.move(target)
        
        elif action in ["status", "状态", "s"]:
            self.player.show_status()
        
        elif action in ["inventory", "背包", "i"]:
            self.show_inventory()
        
        elif action in ["take", "拾取", "get", "pickup"]:
            if not target:
                print("请指定要拾取的物品")
                return
            self.take_item(target)
        
        elif action in ["use", "使用"]:
            if not target:
                print("请指定要使用的物品")
                return
            self.use_item(target)
        
        elif action in ["attack", "攻击", "fight", "战斗"]:
            if not target:
                # 如果没有指定目标，攻击第一个敌人
                if self.current_location.enemies:
                    self.combat(self.current_location.enemies[0])
                else:
                    print("这里没有敌人！")
                return
            self.attack_enemy(target)
        
        elif action in ["help", "帮助", "h", "?"]:
            self.show_help()
        
        elif action in ["quit", "退出", "exit", "q"]:
            self.quit_game()
        
        else:
            print(f"未知指令: {action}. 输入 'help' 查看可用指令。")
    
    def move(self, direction):
        """移动到新地点"""
        direction = direction.strip()
        
        if direction in self.current_location.connections:
            self.current_location = self.current_location.connections[direction]
            self.player.current_location = self.current_location
            
            if not self.current_location.visited:
                self.current_location.visited = True
                print(f"\n你第一次来到了这里...")
            
            self.current_location.describe()
        else:
            print(f"不能往{direction}走！")
    
    def show_inventory(self):
        """显示背包"""
        print("\n" + "="*50)
        print("背包:")
        if not self.player.inventory:
            print("  (空)")
        else:
            for item in self.player.inventory:
                print(f"  - {item.name} ({item.item_type}): {item.description}")
        print("="*50 + "\n")
    
    def take_item(self, item_name):
        """拾取物品"""
        for item in self.current_location.items:
            if item.name.lower() == item_name.lower() or item_name.lower() in item.name.lower():
                self.player.add_item(item)
                self.current_location.items.remove(item)
                print(f"你拾取了 {item.name}")
                return
        
        print(f"这里没有 {item_name}！")
    
    def use_item(self, item_name):
        """使用物品"""
        for item in self.player.inventory:
            if item.name.lower() == item_name.lower() or item_name.lower() in item.name.lower():
                if item.use(self.player):
                    self.player.remove_item(item.name)
                return
        
        print(f"背包里没有 {item_name}！")
    
    def attack_enemy(self, enemy_name):
        """攻击指定敌人"""
        for enemy in self.current_location.enemies:
            if enemy.name.lower() == enemy_name.lower() or enemy_name.lower() in enemy.name.lower():
                self.combat(enemy)
                return
        
        print(f"这里没有 {enemy_name}！")
    
    def combat(self, enemy):
        """战斗系统"""
        print(f"\n⚔️  战斗开始！你遭遇了 {enemy.name}！")
        print(f"{enemy.name}: HP {enemy.hp}/{enemy.max_hp}")
        
        while enemy.is_alive() and self.player.hp > 0:
            print(f"\n你的生命值: {self.player.hp}/{self.player.max_hp}")
            print(f"{enemy.name}的生命值: {enemy.hp}/{enemy.max_hp}")
            print("\n选择行动:")
            print("  1. 攻击")
            print("  2. 使用物品")
            print("  3. 逃跑")
            
            choice = input("请选择 (1-3): ").strip()
            
            if choice == "1":
                # 玩家攻击
                damage = random.randint(self.player.attack - 2, self.player.attack + 5)
                actual_damage = enemy.take_damage(damage)
                print(f"\n你对 {enemy.name} 造成了 {actual_damage} 点伤害！")
                
                if not enemy.is_alive():
                    print(f"\n🎉 你击败了 {enemy.name}！")
                    print(f"获得经验: {enemy.exp_reward}")
                    print(f"获得金币: {enemy.gold_reward}")
                    self.player.gain_exp(enemy.exp_reward)
                    self.player.gold += enemy.gold_reward
                    self.current_location.enemies.remove(enemy)
                    
                    # 检查是否击败了最终boss
                    if enemy.name == "冰霜巨龙":
                        self.win_game()
                    return
                
                # 敌人反击
                enemy_damage = random.randint(enemy.attack - 2, enemy.attack + 3)
                actual_enemy_damage = self.player.take_damage(enemy_damage)
                print(f"{enemy.name} 对你造成了 {actual_enemy_damage} 点伤害！")
                
                if self.player.hp <= 0:
                    self.game_over_screen()
                    return
            
            elif choice == "2":
                # 使用物品
                self.show_inventory()
                item_name = input("使用哪个物品？(输入'取消'返回): ").strip()
                if item_name.lower() not in ["取消", "cancel"]:
                    self.use_item(item_name)
                
                # 敌人攻击
                enemy_damage = random.randint(enemy.attack - 2, enemy.attack + 3)
                actual_enemy_damage = self.player.take_damage(enemy_damage)
                print(f"{enemy.name} 对你造成了 {actual_enemy_damage} 点伤害！")
                
                if self.player.hp <= 0:
                    self.game_over_screen()
                    return
            
            elif choice == "3":
                # 逃跑
                if random.random() < 0.5:
                    print("\n你成功逃脱了！")
                    # 返回上一个地点
                    for direction, location in self.current_location.connections.items():
                        if location.name == "新手村" or not location.enemies:
                            self.current_location = location
                            self.current_location.describe()
                            return
                else:
                    print("\n逃跑失败！")
                    enemy_damage = random.randint(enemy.attack - 2, enemy.attack + 3)
                    actual_enemy_damage = self.player.take_damage(enemy_damage)
                    print(f"{enemy.name} 对你造成了 {actual_enemy_damage} 点伤害！")
                    
                    if self.player.hp <= 0:
                        self.game_over_screen()
                        return
    
    def game_over_screen(self):
        """游戏结束画面"""
        print("\n" + "="*50)
        print("💀 你死了...")
        print(f"最终等级: {self.player.level}")
        print(f"获得经验: {self.player.exp}")
        print(f"收集金币: {self.player.gold}")
        print("="*50)
        self.game_over = True
    
    def win_game(self):
        """通关游戏"""
        print("\n" + "="*50)
        print("🎊 恭喜！你击败了冰霜巨龙，完成了冒险！")
        print(f"最终等级: {self.player.level}")
        print(f"总经验: {self.player.exp}")
        print(f"总金币: {self.player.gold}")
        print("\n感谢游玩！")
        print("="*50)
        self.game_over = True
    
    def quit_game(self):
        """退出游戏"""
        confirm = input("\n确定要退出游戏吗？(y/n): ").strip().lower()
        if confirm in ["y", "yes", "是", "确定"]:
            print("\n感谢游玩！再见！")
            self.game_over = True
    
    def run(self):
        """运行游戏主循环"""
        self.setup_game()
        self.create_character()
        self.show_help()
        self.current_location.describe()
        
        while not self.game_over:
            try:
                command = input("\n> ").strip()
                if command:
                    self.process_command(command)
            except KeyboardInterrupt:
                print("\n")
                self.quit_game()
            except Exception as e:
                print(f"\n错误: {e}")
                print("请重试或输入 'help' 查看帮助")


if __name__ == "__main__":
    game = Game()
    game.run()
