import json
from .base_player import BasePlayer
from ..rpggo import RPGGOClient

class LLMPlayer(BasePlayer):
    """基于LLM的游戏玩家实现"""
    DEFAULT_PLAYER_ID = 'default_player_id'
    
    def __init__(self):
        super().__init__()
        # self.llm_model = llm_model
        # self.rpggo_client = RPGGOClient()
        self.game_meta = None
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
        rpggo_client = RPGGOClient()
        response = rpggo_client.start_game(game_id)
        self.game_meta = self._extract_game_meta(response)
        self.conversation_history = self._init_conversation_history(response)
        self.game_state = self._extract_game_state(response)
        
        # 游戏主循环
        while not self._is_game_over(self.game_state):
            # 获取下一步行动
            action = self.next_action(self.game_state)
            if action['message'] == 'q':
                break

            # 将玩家输入添加到对话历史
            self.conversation_history.append({
                'character_id': self.DEFAULT_PLAYER_ID,
                'name': 'Player',
                'content': action['message']
            })
            
            # 执行行动并获取响应
            response = rpggo_client.send_action(game_id, action['character_id'], action['message'])

            # 更新对话历史
            self.conversation_history = self._update_conversation_history(response)
            
            # 更新游戏状态
            # self.game_state = self._extract_game_state(response)
            
        self._print_conversation_history()
        return self.conversation_history

    def next_action(self, game_state):
        """使用LLM分析游戏状态并决定下一步行动"""
        # prompt = self._construct_game_prompt(game_state)
        # response = self.llm_model.generate(prompt)
        # action = self._parse_llm_response(response)
        input_message = input("Player: ")
        action = {
            'character_id': self.game_meta['chapter']['characters'][0]['character_id'],
            'message': input_message
        }

        return action
    
    def update_state(self, game_state):
        """更新游戏状态"""
        pass
    
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
    
    def _extract_game_meta(self, response):
        """从RPGGO的响应中提取游戏元数据"""
        # 游戏信息
        game_meta = {}
        game_meta['game_id'] = response.get('game_id')
        game_meta['game_name'] = response.get('game_name')
        game_meta['background'] = response.get('background')
        game_meta['introduction'] = response.get('intro')
        game_meta['category'] = response.get('category')
        game_meta['user_id'] = response.get('user_id')
        # 章节信息
        chapter = {}
        chapter['chapter_id'] = response['chapter'].get('chapter_id')
        chapter['name'] = response['chapter'].get('chapter_name')
        chapter['background'] = response['chapter'].get('background')
        chapter['introduction'] = response['chapter'].get('intro')
        chapter['goals'] = response['chapter'].get('goals')
        chapter['goal_info'] = response['chapter'].get('goal_info')
        # 角色信息
        characters = []
        for character in response['chapter']['characters']:
            character_info = {
                'character_id': character.get('id'),
                'character_name': character.get('name'),
                'type': character.get('type'),
                'intro': character.get('intro'),
            }
            characters.append(character_info)

        chapter['characters'] = characters
        game_meta['chapter'] = chapter
        self.game_meta = game_meta
        print(json.dumps(self.game_meta, indent=4, ensure_ascii=False))
        return self.game_meta
    
    def _init_conversation_history(self, response):
        """初始化对话历史"""
        self.conversation_history = []
        for item in response['chapter']['init_dialog']:
            self.conversation_history.append(
                {
                    'character_id': item.get('character_id'),
                    'name': item.get('name'),
                    'content': item.get('message')
                }
            )
            print(f"{item.get('name')}: {item.get('message')}\n\n")
        return self.conversation_history
    
    def _update_conversation_history(self, response):
        """更新对话历史"""
        if not response:
            return self.conversation_history
        # print(json.dumps(response, indent=4, ensure_ascii=False))
        replies = []
        for msg in response:
            if msg.get('character_type') == 'common_npc':
                replies.append(
                    {
                        'character_id': msg.get('character_id'),
                        'name': self._get_character_name(msg.get('character_id')),
                        'content': msg.get('text')
                    }
                )
            elif msg.get('character_type') == 'async_npc':
                replies.append(
                    {
                        'character_id': msg.get('character_id'),
                        'name': self._get_character_name(msg.get('character_id')),
                        'content': msg.get('text')
                    }
                )
        self.conversation_history.extend(replies)
        for reply in replies:
            print(f"{reply['name']}: {reply['content']}\n\n")
        return self.conversation_history
    
    def _extract_game_state(self, response):
        """从RPGGO的响应中提取游戏状态"""
        # 这里需要根据RPGGO的响应格式来实现具体的解析逻辑
        return response
    
    def _is_game_over(self, game_state):
        """判断游戏是否结束"""
        # 根据游戏状态判断是否达到结束条件
        # 可以检查特定的关键词或状态标志
        return False
    
    def _get_character_name(self, character_id):
        """根据角色ID获取角色名称"""
        for character in self.game_meta['chapter']['characters']:
            if character['character_id'] == character_id:
                return character['character_name']
        return None

    def _print_conversation_history(self):
        """打印对话历史"""
        for msg in self.conversation_history:
            print(f"{msg['name']}: {msg['content']}\n\n")
    
    def _format_conversation_history(self):
        """格式化对话历史以包含在提示词中"""
        formatted_history = "\n".join(
            f"Turn {i+1}: {message}" 
            for i, message in enumerate(self.conversation_history[-5:])  # 只使用最近的5轮对话
        )
        return formatted_history 