# -*- coding: utf-8 -*-
"""
This file is the implementation of an AI-based game player.

TODO:
- switch to next chapter
- ...
"""

from pydantic import BaseModel
import json
import random

from ..rpggo import RPGGOClient
from ..utils.llm_utils import GPT
from ..utils.log import get_logger
from .player_prompt import get_system_prompt_tpl_for_ai_player
from ..utils.common import run_function_with_retry

logger = get_logger('LLMPlayer')

class GamePlayConfig(BaseModel):
    """
    define the gameplay config
    """
    game_id: str
    max_turns: int = 10 # max chat turns
    gameplay_instructions: str = "" # instructions for the player


class LLMPlayer():
    """LLM-based game player implementation"""
    DEFAULT_PLAYER_ID = 'default_player_id'
    MAX_HISTORY_LENGTH_FOR_PROMPT = 20
    MAX_GAME_SESSION_TURNS = 30
    MAX_RETRY_COUNT = 3
    
    def __init__(self):
        self.game_meta = None
        self.game_state = self._init_game_state()
        self.conversation_history = []
        
    def play_game(self, gameplay_config: GamePlayConfig):
        """
        Start a complete game session
        
        Args:
            game_id: Unique identifier for the RPGGO game
            
        Returns:
            conversation_history: Complete game dialogue history
        """
        # Initialize game
        rpggo_client = RPGGOClient()
        response = rpggo_client.start_game(gameplay_config.game_id)
        self.game_meta = self._extract_game_meta(response)
        self.conversation_history = self._init_conversation_history(response)
        self.game_state = self._init_game_state()
        
        # Game main loop
        while not self._is_game_over(self.game_state, gameplay_config):
            # Get next action
            action = run_function_with_retry(
                func=lambda: self.next_action(self.game_state, gameplay_config),
                max_retries=self.MAX_RETRY_COUNT,
                error_msg="Failed to generate action"
            )
            if not action:
                break
            if action['message'] == 'q':
                break

            # Add player input to dialogue history
            self.conversation_history.append({
                'character_id': self.DEFAULT_PLAYER_ID,
                'name': 'Player',
                'content': action['message']
            })
            print(f"Player: {action['message']}\n\n")
            
            # Execute action and get response
            response = run_function_with_retry(
                func=lambda: rpggo_client.send_action(gameplay_config.game_id, action['character_id'], action['message']),
                max_retries=self.MAX_RETRY_COUNT,
                error_msg="Failed to send action"
            )

            if not response:
                break

            # Update dialogue history
            self.conversation_history = self._update_conversation_history(response)
            
            # Update game state
            self.game_state = self._update_game_state(response)
            
        self._print_conversation_history()
        return self._export_gameplay_session()

    def next_action(self, game_state, gameplay_config: GamePlayConfig):
        """Use LLM to analyze game state and decide next action"""
        gpt = GPT(model_name="gpt-4o")
        prompt = self._construct_prompt_for_next_action(gameplay_config.gameplay_instructions)
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
        """Update game state"""
        pass

    def _switch_to_next_chapter(self, next_chapter_id):
        """Switch to next chapter"""
        pass
    
    def _construct_prompt_for_next_action(self, gameplay_instructions: str):
        # TODO: add gameplay instructions to the prompt
        participants = [character['character_name'] for character in self.game_meta['chapter']['characters']]
        player_name = "player"
        chat_history = self._format_conversation_history_for_action_generation()
        prompt_tpl = get_system_prompt_tpl_for_ai_player(is_nsfw=False)
        prompt_tpl = prompt_tpl.replace("{$PARTICIPANTS_LIST}", json.dumps(participants, ensure_ascii=False))
        prompt_tpl = prompt_tpl.replace("{$PLAYER_NAME}", player_name)
        prompt_tpl = prompt_tpl.replace("{$GAME_META_INFO}", json.dumps(self.game_meta, ensure_ascii=False))
        prompt_tpl = prompt_tpl.replace("{$INTERACTION_HISTORY}", json.dumps(chat_history, ensure_ascii=False))
        prompt_tpl = prompt_tpl.replace("{$GAME_PLAY_INSTRUCTIONS}", gameplay_instructions)
        return prompt_tpl
    
    def _extract_game_meta(self, response):
        """Extract game metadata from RPGGO response"""
        # Game information
        game_meta = {}
        game_meta['game_id'] = response.get('game_id')
        game_meta['game_name'] = response.get('game_name')
        game_meta['background'] = response.get('background')
        game_meta['introduction'] = response.get('intro')
        game_meta['category'] = response.get('category')
        game_meta['user_id'] = response.get('user_id')
        # Chapter information
        chapter = {}
        chapter['chapter_id'] = response['chapter'].get('chapter_id')
        chapter['name'] = response['chapter'].get('chapter_name')
        chapter['background'] = response['chapter'].get('background')
        chapter['introduction'] = response['chapter'].get('intro')
        chapter['goals'] = response['chapter'].get('goals')
        chapter['goal_info'] = response['chapter'].get('goal_info')
        # Character information
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
        """Initialize conversation history"""
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
        """Update conversation history"""
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
        """Initialize game state"""
        return {
            'chat_turns': 0,
            'end_game': False,
            'goal_status': {}
        }
    
    def _update_game_state(self, response):
        """Extract game state from RPGGO response"""
        for msg in response:
            if msg['result'].get('character_type') == 'common_npc' and msg['result'].get('text'):
                self.game_state['chat_turns'] += 1
                if self.game_state['chat_turns'] >= self.MAX_GAME_SESSION_TURNS:
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
    
    def _is_game_over(self, game_state, gameplay_config: GamePlayConfig):
        return game_state['end_game'] or game_state['chat_turns'] >= gameplay_config.max_turns
    
    def _get_character_name(self, character_id):
        """Get character name by character ID"""
        for character in self.game_meta['chapter']['characters']:
            if character['character_id'] == character_id:
                return character['character_name']
        return None
    
    def _get_character_id(self, character_name):
        """Get character ID by character name"""
        for character in self.game_meta['chapter']['characters']:
            if character['character_name'].lower() == character_name.lower():
                return character['character_id']
        return None

    def _print_conversation_history(self):
        """Print conversation history"""
        for msg in self.conversation_history:
            print(f"{msg['name']}: {msg['content']}\n\n")
    
    def _format_conversation_history_for_action_generation(self):
        """Format conversation history for prompt"""
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
    
    def _export_gameplay_session(self):
        gameplay_session = []
        for msg in self.conversation_history:
            msg_dict = msg.copy()
            msg_dict.pop('character_id')
            gameplay_session.append(msg_dict)
        return gameplay_session
