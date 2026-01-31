"""
图形界面 - GUI组件
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random

from .game_engine import GameEngine
from .models import Player


class GameGUI:
    """游戏图形界面"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("文字RPG冒险游戏")
        self.root.geometry("1000x700")
        self.root.resizable(False, False)
        
        self.game_engine = GameEngine()
        self.player = None
        self.current_location = None
        self.game_over = False
        self.in_combat = False
        self.current_enemy = None
        
        self.setup_ui()
        self.start_game()
    
    def setup_ui(self):
        """设置用户界面"""
        # 配置 ttk 样式
        style = ttk.Style()
        style.theme_use('default')
        
        # 配置按钮样式
        style.configure('Action.TButton',
                       font=('Arial', 10, 'bold'),
                       padding=5)
        
        # 主容器
        main_frame = tk.Frame(self.root, bg="#2b2b2b")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 顶部：标题
        title_label = tk.Label(main_frame, text="🗡️ 文字RPG冒险游戏 🛡️", 
                               font=("Arial", 20, "bold"), bg="#2b2b2b", fg="#FFD700")
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 10))
        
        # 左侧：游戏文本区域
        left_frame = tk.Frame(main_frame, bg="#2b2b2b")
        left_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        
        # 游戏文本显示
        text_label = tk.Label(left_frame, text="游戏信息", font=("Arial", 12, "bold"), 
                             bg="#2b2b2b", fg="#FFFFFF")
        text_label.pack(anchor="w")
        
        self.game_text = scrolledtext.ScrolledText(left_frame, width=60, height=25, 
                                                   font=("Consolas", 10), bg="#1e1e1e", 
                                                   fg="#00FF00", insertbackground="#00FF00",
                                                   wrap=tk.WORD, state=tk.DISABLED)
        self.game_text.pack(fill=tk.BOTH, expand=True)
        
        # 输入区域
        input_frame = tk.Frame(left_frame, bg="#2b2b2b")
        input_frame.pack(fill=tk.X, pady=(10, 0))
        
        tk.Label(input_frame, text="指令:", font=("Arial", 10), 
                bg="#2b2b2b", fg="#FFFFFF").pack(side=tk.LEFT, padx=(0, 5))
        
        self.command_entry = tk.Entry(input_frame, font=("Consolas", 10), 
                                     bg="#1e1e1e", fg="#00FF00", 
                                     insertbackground="#00FF00")
        self.command_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.command_entry.bind("<Return>", lambda e: self.process_command())
        
        submit_btn = ttk.Button(input_frame, text="执行", 
                               command=self.process_command,
                               style='Action.TButton',
                               cursor="hand2")
        submit_btn.pack(side=tk.LEFT, padx=2)
        
        # 右侧：状态和控制面板
        right_frame = tk.Frame(main_frame, bg="#2b2b2b")
        right_frame.grid(row=1, column=1, sticky="nsew")
        
        # 角色状态
        status_label = tk.Label(right_frame, text="角色状态", font=("Arial", 12, "bold"),
                               bg="#2b2b2b", fg="#FFFFFF")
        status_label.pack(anchor="w", pady=(0, 5))
        
        self.status_text = tk.Text(right_frame, width=35, height=10, 
                                  font=("Consolas", 9), bg="#1e1e1e", 
                                  fg="#FFD700", state=tk.DISABLED)
        self.status_text.pack(fill=tk.X, pady=(0, 10))
        
        # 地图显示
        map_label = tk.Label(right_frame, text="地图", font=("Arial", 12, "bold"),
                            bg="#2b2b2b", fg="#FFFFFF")
        map_label.pack(anchor="w", pady=(0, 5))
        
        self.map_canvas = tk.Canvas(right_frame, width=320, height=240, 
                                   bg="#1e1e1e", highlightthickness=0)
        self.map_canvas.pack(pady=(0, 10))
        
        # 快速操作按钮
        actions_label = tk.Label(right_frame, text="快速操作", font=("Arial", 12, "bold"),
                                bg="#2b2b2b", fg="#FFFFFF")
        actions_label.pack(anchor="w", pady=(0, 5))
        
        btn_frame = tk.Frame(right_frame, bg="#2b2b2b")
        btn_frame.pack(fill=tk.X)
        
        # 创建按钮网格
        buttons = [
            ("观察", "look"), ("状态", "status"), ("背包", "inventory"),
            ("北", "go 北"), ("南", "go 南"), ("东", "go 东"),
            ("西", "go 西"), ("攻击", "attack"), ("帮助", "help")
        ]
        
        for i, (text, cmd) in enumerate(buttons):
            btn = ttk.Button(btn_frame, text=text, 
                           command=lambda c=cmd: self.quick_command(c),
                           style='Action.TButton',
                           cursor="hand2",
                           width=10)
            btn.grid(row=i//3, column=i%3, padx=3, pady=3, sticky="ew")
        
        # 配置网格权重
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=3)
        main_frame.grid_columnconfigure(1, weight=1)
        
        for i in range(3):
            btn_frame.grid_columnconfigure(i, weight=1)
    
    def write_to_game_text(self, text, clear=False):
        """写入游戏文本"""
        self.game_text.config(state=tk.NORMAL)
        if clear:
            self.game_text.delete(1.0, tk.END)
        self.game_text.insert(tk.END, text + "\n")
        self.game_text.see(tk.END)
        self.game_text.config(state=tk.DISABLED)
    
    def update_status(self):
        """更新状态显示"""
        if self.player:
            self.status_text.config(state=tk.NORMAL)
            self.status_text.delete(1.0, tk.END)
            self.status_text.insert(1.0, self.player.get_status_text())
            self.status_text.config(state=tk.DISABLED)
    
    def draw_map(self):
        """绘制地图"""
        self.map_canvas.delete("all")
        
        # 地图坐标 (x, y)
        locations_pos = {
            "新手村": (160, 180),
            "迷雾森林": (160, 100),
            "黑暗洞穴": (240, 100),
            "古老遗迹": (80, 100),
            "雪山顶峰": (240, 20)
        }
        
        # 绘制连接线
        connections = [
            ("新手村", "迷雾森林"),
            ("迷雾森林", "黑暗洞穴"),
            ("迷雾森林", "古老遗迹"),
            ("黑暗洞穴", "雪山顶峰")
        ]
        
        for loc1, loc2 in connections:
            x1, y1 = locations_pos[loc1]
            x2, y2 = locations_pos[loc2]
            self.map_canvas.create_line(x1, y1, x2, y2, fill="#666666", width=2)
        
        # 绘制地点
        for loc_name, (x, y) in locations_pos.items():
            if loc_name == self.current_location.name:
                # 当前位置 - 高亮
                color = "#FFD700"
                radius = 18
            elif self.game_engine.locations[loc_name].visited:
                # 已访问 - 绿色
                color = "#4CAF50"
                radius = 15
            else:
                # 未访问 - 灰色
                color = "#888888"
                radius = 15
            
            self.map_canvas.create_oval(x-radius, y-radius, x+radius, y+radius, 
                                       fill=color, outline="#FFFFFF", width=2)
            
            # 地点名称
            name_short = loc_name[:2] if len(loc_name) > 2 else loc_name
            self.map_canvas.create_text(x, y, text=name_short, 
                                       font=("Arial", 8, "bold"), fill="#000000")
            
            # 标记敌人
            if self.game_engine.locations[loc_name].enemies:
                self.map_canvas.create_text(x, y-25, text="⚔", 
                                          font=("Arial", 12), fill="#FF0000")
    
    def start_game(self):
        """开始游戏"""
        self.current_location = self.game_engine.setup_world()
        
        # 创建角色名称输入对话框
        dialog = tk.Toplevel(self.root)
        dialog.title("创建角色")
        dialog.geometry("300x150")
        dialog.resizable(False, False)
        dialog.grab_set()
        
        # 居中显示
        dialog.transient(self.root)
        x = (dialog.winfo_screenwidth() - 300) // 2
        y = (dialog.winfo_screenheight() - 150) // 2
        dialog.geometry(f"+{x}+{y}")
        
        tk.Label(dialog, text="欢迎来到文字冒险世界！", 
                font=("Arial", 12, "bold")).pack(pady=(20, 10))
        
        tk.Label(dialog, text="请输入你的角色名字:", 
                font=("Arial", 10)).pack(pady=(0, 5))
        
        name_entry = tk.Entry(dialog, font=("Arial", 10), width=20)
        name_entry.pack(pady=(0, 10))
        name_entry.focus()
        
        def create_character():
            name = name_entry.get().strip()
            self.player = self.game_engine.create_player(name)
            self.player.current_location = self.current_location
            self.current_location.visited = True
            
            dialog.destroy()
            
            # 显示欢迎信息
            welcome_text = f"""{'='*50}
欢迎来到文字冒险世界！
{'='*50}

欢迎你，{self.player.name}！
你的冒险即将开始...

{self.player.get_status_text()}

{self.current_location.get_description()}

输入 'help' 查看可用指令
"""
            self.write_to_game_text(welcome_text)
            self.update_status()
            self.draw_map()
        
        name_entry.bind("<Return>", lambda e: create_character())
        
        start_btn = ttk.Button(dialog, text="开始冒险", command=create_character,
                              style='Action.TButton', cursor="hand2")
        start_btn.pack(pady=(0, 10))
    
    def quick_command(self, command):
        """快速指令"""
        self.command_entry.delete(0, tk.END)
        self.command_entry.insert(0, command)
        self.process_command()
    
    def process_command(self):
        """处理玩家命令"""
        if not self.player or self.game_over:
            return
        
        command = self.command_entry.get().strip()
        self.command_entry.delete(0, tk.END)
        
        if not command:
            return
        
        self.write_to_game_text(f"\n> {command}")
        
        parts = command.lower().split(maxsplit=1)
        action = parts[0]
        target = parts[1] if len(parts) > 1 else None
        
        if action in ["look", "观察", "l"]:
            self.write_to_game_text(self.current_location.get_description())
        
        elif action in ["go", "前往", "走", "move"]:
            if not target:
                self.write_to_game_text("请指定方向（北/南/东/西）")
                return
            self.move(target)
        
        elif action in ["status", "状态", "s"]:
            self.write_to_game_text(self.player.get_status_text())
        
        elif action in ["inventory", "背包", "i"]:
            self.show_inventory()
        
        elif action in ["take", "拾取", "get", "pickup"]:
            if not target:
                self.write_to_game_text("请指定要拾取的物品")
                return
            self.take_item(target)
        
        elif action in ["use", "使用", "2"]:
            if not target:
                if self.in_combat:
                    self.show_inventory()
                    self.write_to_game_text("请输入 'use <物品名>' 来使用物品")
                else:
                    self.write_to_game_text("请指定要使用的物品")
                return
            self.use_item(target)
            if self.in_combat:
                # 在战斗中使用物品后，敌人攻击
                enemy = self.current_enemy
                if enemy and enemy.is_alive():
                    enemy_damage = random.randint(enemy.attack - 2, enemy.attack + 3)
                    actual_enemy_damage = self.player.take_damage(enemy_damage)
                    self.write_to_game_text(f"{enemy.name} 对你造成了 {actual_enemy_damage} 点伤害！")
                    
                    if self.player.hp <= 0:
                        self.game_over_screen()
                        return
                    
                    status = f"\n你的生命值: {self.player.hp}/{self.player.max_hp}\n{enemy.name}的生命值: {enemy.hp}/{enemy.max_hp}"
                    self.write_to_game_text(status)
        
        elif action in ["attack", "攻击", "fight", "战斗", "1"]:
            if self.in_combat:
                self.combat_action("attack")
                return
            if not target:
                if self.current_location.enemies:
                    self.start_combat(self.current_location.enemies[0])
                else:
                    self.write_to_game_text("这里没有敌人！")
                return
            self.attack_enemy(target)
        
        elif action in ["flee", "逃跑", "3"]:
            if self.in_combat:
                self.combat_action("flee")
            else:
                self.write_to_game_text("你不在战斗中！")
        
        elif action in ["help", "帮助", "h", "?"]:
            self.show_help()
        
        elif action in ["quit", "退出", "exit", "q"]:
            self.quit_game()
        
        else:
            self.write_to_game_text(f"未知指令: {action}. 输入 'help' 查看可用指令。")
        
        self.update_status()
    
    def show_help(self):
        """显示帮助信息"""
        help_text = """
{'='*50}
游戏指令:
  look/观察    - 查看当前位置
  go/前往 <方向> - 前往指定方向（北/南/东/西）
  status/状态  - 查看角色状态
  inventory/背包 - 查看背包
  take/拾取 <物品> - 拾取物品
  use/使用 <物品> - 使用物品
  attack/攻击 <敌人> - 攻击敌人
  help/帮助    - 显示帮助信息
  quit/退出    - 退出游戏
{'='*50}
"""
        self.write_to_game_text(help_text)
    
    def move(self, direction):
        """移动到新地点"""
        direction = direction.strip()
        
        if direction in self.current_location.connections:
            self.current_location = self.current_location.connections[direction]
            self.player.current_location = self.current_location
            
            if not self.current_location.visited:
                self.current_location.visited = True
                self.write_to_game_text("\n你第一次来到了这里...")
            
            self.write_to_game_text(self.current_location.get_description())
            self.draw_map()
        else:
            self.write_to_game_text(f"不能往{direction}走！")
    
    def show_inventory(self):
        """显示背包"""
        inv_text = "\n" + "="*40 + "\n背包:\n"
        if not self.player.inventory:
            inv_text += "  (空)\n"
        else:
            for item in self.player.inventory:
                inv_text += f"  - {item.name} ({item.item_type}): {item.description}\n"
        inv_text += "="*40
        self.write_to_game_text(inv_text)
    
    def take_item(self, item_name):
        """拾取物品"""
        for item in self.current_location.items:
            if item.name.lower() == item_name.lower() or item_name.lower() in item.name.lower():
                self.player.add_item(item)
                self.current_location.items.remove(item)
                self.write_to_game_text(f"你拾取了 {item.name}")
                return
        
        self.write_to_game_text(f"这里没有 {item_name}！")
    
    def use_item(self, item_name):
        """使用物品"""
        for item in self.player.inventory:
            if item.name.lower() == item_name.lower() or item_name.lower() in item.name.lower():
                result = item.use(self.player)
                if isinstance(result, tuple):
                    msg, should_remove = result
                    self.write_to_game_text(msg)
                    if should_remove:
                        self.player.remove_item(item.name)
                else:
                    self.write_to_game_text(result)
                self.update_status()
                return
        
        self.write_to_game_text(f"背包里没有 {item_name}！")
    
    def attack_enemy(self, enemy_name):
        """攻击指定敌人"""
        for enemy in self.current_location.enemies:
            if enemy.name.lower() == enemy_name.lower() or enemy_name.lower() in enemy.name.lower():
                self.start_combat(enemy)
                return
        
        self.write_to_game_text(f"这里没有 {enemy_name}！")
    
    def start_combat(self, enemy):
        """开始战斗"""
        self.in_combat = True
        self.current_enemy = enemy
        
        combat_text = f"""
⚔️  战斗开始！你遭遇了 {enemy.name}！
{enemy.name}: HP {enemy.hp}/{enemy.max_hp}

选择行动:
  1. 攻击 - 输入 'attack' 或 '1'
  2. 使用物品 - 输入 'use <物品名>' 或 '2'
  3. 逃跑 - 输入 'flee' 或 '3'
"""
        self.write_to_game_text(combat_text)
    
    def combat_action(self, action, item_name=None):
        """战斗行动"""
        if not self.in_combat or not self.current_enemy:
            return
        
        enemy = self.current_enemy
        
        if action == "attack":
            # 玩家攻击
            damage = random.randint(self.player.attack - 2, self.player.attack + 5)
            actual_damage = enemy.take_damage(damage)
            self.write_to_game_text(f"\n你对 {enemy.name} 造成了 {actual_damage} 点伤害！")
            
            if not enemy.is_alive():
                combat_result = f"""
🎉 你击败了 {enemy.name}！
获得经验: {enemy.exp_reward}
获得金币: {enemy.gold_reward}
"""
                self.write_to_game_text(combat_result)
                
                old_level = self.player.level
                self.player.gain_exp(enemy.exp_reward)
                self.player.gold += enemy.gold_reward
                self.current_location.enemies.remove(enemy)
                
                # 检查是否升级
                if self.player.level > old_level:
                    level_up_msg = f"""
🎉 恭喜！你升到了 {self.player.level} 级！
   生命值上限: {self.player.max_hp}
   攻击力: {self.player.attack}
   防御力: {self.player.defense}
"""
                    self.write_to_game_text(level_up_msg)
                
                # 检查是否击败了最终boss
                if enemy.name == "冰霜巨龙":
                    self.win_game()
                
                self.in_combat = False
                self.current_enemy = None
                self.update_status()
                self.draw_map()
                return
            
            # 敌人反击
            enemy_damage = random.randint(enemy.attack - 2, enemy.attack + 3)
            actual_enemy_damage = self.player.take_damage(enemy_damage)
            self.write_to_game_text(f"{enemy.name} 对你造成了 {actual_enemy_damage} 点伤害！")
            
            if self.player.hp <= 0:
                self.game_over_screen()
                return
            
            # 显示状态
            status = f"\n你的生命值: {self.player.hp}/{self.player.max_hp}\n{enemy.name}的生命值: {enemy.hp}/{enemy.max_hp}"
            self.write_to_game_text(status)
        
        elif action == "flee":
            # 逃跑
            if random.random() < 0.5:
                self.write_to_game_text("\n你成功逃脱了！")
                self.in_combat = False
                self.current_enemy = None
                
                # 返回上一个地点
                for direction, location in self.current_location.connections.items():
                    if location.name == "新手村" or not location.enemies:
                        self.current_location = location
                        self.write_to_game_text(self.current_location.get_description())
                        self.draw_map()
                        return
            else:
                self.write_to_game_text("\n逃跑失败！")
                enemy_damage = random.randint(enemy.attack - 2, enemy.attack + 3)
                actual_enemy_damage = self.player.take_damage(enemy_damage)
                self.write_to_game_text(f"{enemy.name} 对你造成了 {actual_enemy_damage} 点伤害！")
                
                if self.player.hp <= 0:
                    self.game_over_screen()
                    return
        
        self.update_status()
    
    def game_over_screen(self):
        """游戏结束画面"""
        game_over_text = f"""
{'='*50}
💀 你死了...
最终等级: {self.player.level}
获得经验: {self.player.exp}
收集金币: {self.player.gold}
{'='*50}
"""
        self.write_to_game_text(game_over_text)
        self.game_over = True
        self.in_combat = False
        
        messagebox.showinfo("游戏结束", "你的冒险结束了...")
    
    def win_game(self):
        """通关游戏"""
        win_text = f"""
{'='*50}
🎊 恭喜！你击败了冰霜巨龙，完成了冒险！
最终等级: {self.player.level}
总经验: {self.player.exp}
总金币: {self.player.gold}

感谢游玩！
{'='*50}
"""
        self.write_to_game_text(win_text)
        self.game_over = True
        self.in_combat = False
        
        messagebox.showinfo("胜利！", "恭喜你完成了冒险！")
    
    def quit_game(self):
        """退出游戏"""
        if messagebox.askyesno("退出游戏", "确定要退出游戏吗？"):
            self.root.quit()
