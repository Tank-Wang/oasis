from abc import ABC, abstractmethod

class BasePlayer(ABC):
    """抽象基类，定义AI游戏玩家的基本接口"""
    
    def __init__(self):
        self.game_state = None
    
    @abstractmethod
    def next_action(self, game_state):
        """
        根据当前游戏状态决定下一步行动
        
        Args:
            game_state: 当前游戏状态的表示
            
        Returns:
            action: 返回选择的行动
        """
        pass
    
    @abstractmethod
    def update_state(self, game_state):
        """
        更新玩家内部的游戏状态
        
        Args:
            game_state: 新的游戏状态
        """
        pass 