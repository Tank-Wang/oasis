from abc import ABC, abstractmethod

class BaseEvaluator(ABC):
    """抽象基类，定义游戏评估器的基本接口"""
    
    @abstractmethod
    def evaluate_game(self, game_history):
        """
        评估一局完整的游戏
        
        Args:
            game_history: 游戏历史记录
            
        Returns:
            evaluation: 返回评估结果
        """
        pass
    
    @abstractmethod
    def evaluate_move(self, game_state, action):
        """
        评估单个行动的质量
        
        Args:
            game_state: 行动发生时的游戏状态
            action: 采取的行动
            
        Returns:
            score: 行动的评分
        """
        pass 