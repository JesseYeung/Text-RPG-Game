"""
地点类
"""


class Location:
    """游戏地点"""
    
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
    
    def get_description(self):
        """获取地点描述"""
        desc = f"\n📍 {self.name}\n{self.description}\n"
        
        if self.items:
            desc += f"\n💎 你看到了: {', '.join([item.name for item in self.items])}"
        
        if self.enemies:
            desc += f"\n⚠️  这里有敌人: {', '.join([enemy.name for enemy in self.enemies])}"
        
        if self.connections:
            desc += f"\n🧭 可前往: {', '.join(self.connections.keys())}"
        
        return desc
