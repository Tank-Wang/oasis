from .base_player import BasePlayer
from ..rpggo import RPGGOClient

class LLMPlayer(BasePlayer):
    """基于LLM的游戏玩家实现"""
    
    def __init__(self, llm_model, rpggo_client):
        super().__init__()
        self.llm_model = llm_model
        self.rpggo_client = rpggo_client
        self.game_state = None
        self.conversation_history = []
        
    def play_game(self, game_id):
        """
        开始一个完整的游戏会话
        
        Args:
            game_id: RPGGO游戏的唯一标识符
            
        Returns:
            conversation_history: 完整的游戏对话历史
        """
        # 初始化游戏
        response = self.rpggo_client.start_game(game_id)
        self.conversation_history = [response]
        self.game_state = self._extract_game_state(response)
        
        # 游戏主循环
        while not self._is_game_over(self.game_state):
            # 获取下一步行动
            action = self.next_action(self.game_state)
            
            # 执行行动并获取响应
            response = self.rpggo_client.send_action(game_id, action)
            self.conversation_history.append(response)
            
            # 更新游戏状态
            self.game_state = self._extract_game_state(response)
            
        return self.conversation_history

    def next_action(self, game_state):
        """使用LLM分析游戏状态并决定下一步行动"""
        prompt = self._construct_game_prompt(game_state)
        response = self.llm_model.generate(prompt)
        action = self._parse_llm_response(response)
        return action
    
    def _construct_game_prompt(self, game_state):
        """构建向LLM描述游戏状态的提示词"""
        prompt = f"""
        当前游戏状态:
        {game_state}
        
        游戏对话历史:
        {self._format_conversation_history()}
        
        作为一个RPG游戏玩家，请基于当前状态和对话历史，决定下一步最合适的行动。
        你的回答应该是一个具体的行动指令。
        """
        return prompt
    
    def _parse_llm_response(self, response):
        """将LLM的响应解析为具体的游戏行动"""
        # 清理和标准化LLM的响应
        action = response.strip()
        # 可以添加更多的响应处理逻辑
        return action
    
    def _extract_game_state(self, response):
        """从RPGGO的响应中提取游戏状态"""
        # 这里需要根据RPGGO的响应格式来实现具体的解析逻辑
        return response
    
    def _is_game_over(self, game_state):
        """判断游戏是否结束"""
        # 根据游戏状态判断是否达到结束条件
        # 可以检查特定的关键词或状态标志
        return False
    
    def _format_conversation_history(self):
        """格式化对话历史以包含在提示词中"""
        formatted_history = "\n".join(
            f"Turn {i+1}: {message}" 
            for i, message in enumerate(self.conversation_history[-5:])  # 只使用最近的5轮对话
        )
        return formatted_history 