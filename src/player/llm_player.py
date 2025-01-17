import json
import random
from .base_player import BasePlayer
from ..rpggo import RPGGOClient
from ..utils.llm_utils import GPT
from ..utils.log import get_logger
from ..player.prompt import get_system_prompt_tpl_for_ai_player
from ..utils.common import run_function_with_retry

logger = get_logger('LLMPlayer')

class LLMPlayer(BasePlayer):
    """基于LLM的游戏玩家实现"""
    DEFAULT_PLAYER_ID = 'default_player_id'
    MAX_HISTORY_LENGTH_FOR_PROMPT = 20
    MAX_CHAT_TURNS = 10
    MAX_RETRY_COUNT = 3
    
    def __init__(self):
        super().__init__()
        # self.llm_model = llm_model
        # self.rpggo_client = RPGGOClient()
        self.game_meta = None
        self.game_state = self._init_game_state()
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
        self.game_state = self._init_game_state()
        
        # 游戏主循环
        retry_count = 0
        while not self._is_game_over(self.game_state):
            # 获取下一步行动
            action = run_function_with_retry(
                func=lambda: self.next_action(self.game_state),
                max_retries=self.MAX_RETRY_COUNT,
                error_msg="Failed to generate action"
            )
            if not action:
                break
            if action['message'] == 'q':
                break

            # 将玩家输入添加到对话历史
            self.conversation_history.append({
                'character_id': self.DEFAULT_PLAYER_ID,
                'name': 'Player',
                'content': action['message']
            })
            print(f"Player: {action['message']}\n\n")
            
            # 执行行动并获取响应
            response = run_function_with_retry(
                func=lambda: rpggo_client.send_action(game_id, action['character_id'], action['message']),
                max_retries=self.MAX_RETRY_COUNT,
                error_msg="Failed to send action"
            )

            if not response:
                break

            # 更新对话历史
            self.conversation_history = self._update_conversation_history(response)
            
            # 更新游戏状态
            self.game_state = self._update_game_state(response)
            
        self._print_conversation_history()
        return self.conversation_history

    def next_action(self, game_state):
        """使用LLM分析游戏状态并决定下一步行动"""
        gpt = GPT(model_name="gpt-4o-mini")
        prompt = self._construct_prompt_for_next_action()
        logger.debug(f"prompt for next action: {prompt}")

        try:
            response = gpt.generate(prompt=prompt, json_mode=True)
            logger.debug(f"response for next action: {response}")
            json_result = json.loads(response)
            action_options = json_result.get("action_options", [])
            action_list = []
            for action in action_options:
                character_name = action.get("character_to_address")
                character_id = self._get_character_id(character_name)
                action_list.append(
                    {
                        "character_id": character_id,
                        "character_name": character_name,
                        "message": action["action_detail"],
                    }
                )
            if action_list:
                random.shuffle(action_list)
                return action_list[0]
            else:
                return None

        except json.JSONDecodeError as e:
            logger.error(f"failed to parse json response, error: {e}")
            logger.error(f"response is: {response.result}")
            return None
        except Exception as e:
            logger.error(f"failed to generate action, error: {e}")
            return None
    
    def update_state(self, game_state):
        """更新游戏状态"""
        pass

    def _switch_to_next_chapter(self, next_chapter_id):
        """切换到下一个章节"""
        pass
    
    def _construct_prompt_for_next_action(self):
        participants = [character['character_name'] for character in self.game_meta['chapter']['characters']]
        player_name = "player"
        chat_history = self._format_conversation_history()
        prompt_tpl = get_system_prompt_tpl_for_ai_player(is_nsfw=False)
        prompt_tpl = prompt_tpl.replace("{$PARTICIPANTS_LIST}", json.dumps(participants, ensure_ascii=False))
        prompt_tpl = prompt_tpl.replace("{$PLAYER_NAME}", player_name)
        prompt_tpl = prompt_tpl.replace("{$GAME_META_INFO}", json.dumps(self.game_meta, ensure_ascii=False))
        prompt_tpl = prompt_tpl.replace("{$INTERACTION_HISTORY}", json.dumps(chat_history, ensure_ascii=False))
        return prompt_tpl
    
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
        # print(json.dumps(self.game_meta, indent=4, ensure_ascii=False))
        return self.game_meta
    
    def _init_conversation_history(self, response):
        """初始化对话历史"""
        # logger.debug(f"init conversation history: {json.dumps(response, indent=4, ensure_ascii=False)}")
        self.conversation_history = []
        for item in response['chapter'].get('init_dialog', []):
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
            if msg['result'].get('character_type') == 'common_npc':
                replies.append(
                    {
                        'character_id': msg['result'].get('character_id'),
                        'name': self._get_character_name(msg['result'].get('character_id')),
                        'content': msg['result'].get('text')
                    }
                )
            elif msg['result'].get('character_type') == 'async_npc':
                if msg['result'].get('text').strip():
                    replies.append(
                        {
                            'character_id': msg['result'].get('character_id'),
                        'name': self._get_character_name(msg['result'].get('character_id')),
                        'content': msg['result'].get('text')
                    }
                )
        self.conversation_history.extend(replies)
        for reply in replies:
            print(f"{reply['name']}: {reply['content']}\n\n")
        return self.conversation_history
    
    def _init_game_state(self):
        """初始化游戏状态"""
        return {
            'chat_turns': 0,
            'end_game': False,
            'goal_status': {}
        }
    
    def _update_game_state(self, response):
        """从RPGGO的响应中提取游戏状态"""
        for msg in response:
            if msg['result'].get('character_type') == 'common_npc' and msg['result'].get('text'):
                self.game_state['chat_turns'] += 1
                if self.game_state['chat_turns'] >= self.MAX_CHAT_TURNS:
                    self.game_state['end_game'] = True
            elif msg['result'].get('character_type') == 'goal_check_dm':
                self.game_state['goal_status'] = msg['game_status']['goal']['goals_status']
                status_action = msg['game_status']['action']
                if status_action in [3, 4]:
                    self.game_state['end_game'] = True
                elif status_action == 2:
                    next_chapter_id = msg['game_status']['chapter_id']
                    self._switch_to_next_chapter(next_chapter_id)
                    # TODO: switch to next chapter
                    pass
        return self.game_state
    
    def _is_game_over(self, game_state):
        return game_state['end_game']
    
    def _get_character_name(self, character_id):
        """根据角色ID获取角色名称"""
        for character in self.game_meta['chapter']['characters']:
            if character['character_id'] == character_id:
                return character['character_name']
        return None
    
    def _get_character_id(self, character_name):
        """根据角色名称获取角色ID"""
        for character in self.game_meta['chapter']['characters']:
            if character['character_name'].lower() == character_name.lower():
                return character['character_id']
        return None

    def _print_conversation_history(self):
        """打印对话历史"""
        for msg in self.conversation_history:
            print(f"{msg['name']}: {msg['content']}\n\n")
    
    def _format_conversation_history(self):
        """格式化对话历史以包含在提示词中"""
        formatted_history = []
        for msg in self.conversation_history[:self.MAX_HISTORY_LENGTH_FOR_PROMPT]:
            if msg['name'] == 'player':
                formatted_history.append({
                    'role': 'you',
                    'content': msg['content']
                })
            else:
                formatted_history.append({
                    'role': msg['name'],
                    'content': msg['content']
                })
        return formatted_history 