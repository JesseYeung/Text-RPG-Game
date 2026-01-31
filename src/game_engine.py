"""
游戏引擎 - 核心游戏逻辑
"""
from .models import Player, Enemy, Location, HealingPotion, Weapon


class GameEngine:
    """游戏引擎 - 处理游戏世界和逻辑"""
    
    def __init__(self):
        self.locations = {}
        self.start_location = None
    
    def setup_world(self):
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
        
        self.start_location = village
        return village
    
    def create_player(self, name):
        """创建玩家"""
        if not name:
            name = "冒险者"
        return Player(name)
