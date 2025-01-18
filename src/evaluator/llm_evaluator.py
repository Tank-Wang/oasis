# -*- coding: utf-8 -*-
"""
This file is the implementation of an LLM-based game evaluator.

TODO:
- add apple-to-apple evaluation
- update evaluator prompt
"""


import json
from typing import List, Dict
from ..utils.llm_utils import GPT
from ..utils.log import get_logger
from .evaluator_prompt import EVALUATOR_PROMPT

logger = get_logger('LLMEvaluator')

class LLMEvaluator():
    """基于LLM的游戏评估器实现，专注于评估NPC表现和游戏可玩性"""
    
    def __init__(self):
        pass
    
    def evaluate_game(self, game_metadata: Dict, game_histories: List[Dict]) -> Dict:
        """
        基于多次游戏对话历史评估游戏表现

        Args:
            game_metadata: 游戏元数据
            game_histories: 包含多次游戏对话历史的列表，每个元素是一次完整的对话历史
            
        Returns:
            evaluation: 包含评估结果的字典
        """
        if not game_metadata:
            raise ValueError("game_metadata is empty")

        if not game_histories:
            raise ValueError("conversation_history is empty")
        
        if len(game_histories) < 3:
            logger.warning("conversation_history is less than 3, recommend to include more conversation_history")
 
        # 构建评估提示词
        prompt = self._construct_game_evaluation_prompt(game_metadata, game_histories)
        logger.info(f"evaluator prompt: {prompt}")
        
        # 获取LLM的评估结果
        gpt = GPT(model_name="gpt-4o")
        try:
            response = gpt.generate(prompt=prompt, json_mode=True)
            evaluation = json.loads(response)
            logger.info(f"evaluation: {json.dumps(evaluation, ensure_ascii=False, indent=4)}")
        except json.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"Error in GPT generate: {str(e)}")
            return {}

        return evaluation
    
    def _construct_game_evaluation_prompt(self, game_metadata: Dict, gameplay_sessions: List[Dict]) -> str:
        """构建评估提示词"""
        prompt_tpl = EVALUATOR_PROMPT
        game_metadata_for_evaluation = self._get_game_metadata_for_evaluation(game_metadata)
        logger.info(f"game_metadata_for_evaluation: {json.dumps(game_metadata_for_evaluation, ensure_ascii=False, indent=2)}")
        prompt = prompt_tpl.replace('{$GAME_METADATA}', json.dumps(game_metadata_for_evaluation, ensure_ascii=False))
        prompt = prompt.replace('{$CHAT_HISTORY}', json.dumps(gameplay_sessions, ensure_ascii=False))
        return prompt

    def _get_game_metadata_for_evaluation(self, game_metadata: Dict) -> Dict:
        if game_metadata['category'] == 'solo-character':
            return self._get_game_metadata_for_solo_character(game_metadata)
        else:
            return self._get_game_metadata_for_game(game_metadata)
        
    def _get_game_metadata_for_solo_character(self, game_metadata: Dict) -> Dict:
        game_dict = {}
        game_dict['category'] = 'solo-character'
        character = game_metadata['chapters'][0]['characters'][0]
        game_dict['character_name'] = character['name']
        game_dict['background'] = character['background']
        game_dict['intro'] = character['intro']
        game_dict['appearance'] = character['appearance']
        game_dict['traits'] = character['traits']
        game_dict['tone'] = character['tone']
        game_dict['response_emojis'] = character['response_emojis']
        game_dict['response_gestures'] = character['response_gestures']
        game_dict['character_tags'] = character['character_tags']
        game_dict['opening_line'] = character['opening_line']
        if character['module_details']:
            modules = []
            for module in character['module_details']:
                module_dict = {
                    'name': module['name'],
                    'category': module['category'],
                    'entries': [entry.pop('entrie_id') for entry in module['entries']]
                }
                modules.append(module_dict)
            game_dict['modules'] = modules
        return game_dict

    def _get_game_metadata_for_game(self, game_metadata: Dict) -> Dict:
        game_dict = {}
        game_dict['name'] = game_metadata['name']
        game_dict['background'] = game_metadata['background']
        game_dict['intro'] = game_metadata['intro']
        game_dict['mechanics'] = game_metadata['mechanics']
        game_dict['game_tags'] = game_metadata['game_tags']

        if game_metadata['worlds']:
            world_dict = {}
            world_dict['name'] = game_metadata['worlds'][0]['name']
            world_dict['world_view'] = game_metadata['worlds'][0]['world_view']
            world_dict['knowledge_details'] = game_metadata['worlds'][0]['knowledge_details']
            if world_dict['name'] or world_dict['world_view']:
                game_dict['world'] = world_dict

        chapters = []
        for chapter in game_metadata['chapters'][:3]:
            chapter_dict = {}
            chapter_dict['name'] = chapter['name']
            chapter_dict['background'] = chapter['background']
            chapter_dict['goals'] = chapter['goals']
            chapter_dict['endings'] = chapter['endings']

            # characters
            characters = []
            for character in chapter['characters']:
                character_dict = {}
                character_dict['name'] = character['name']
                character_dict['type'] = character['type']
                character_dict['background'] = character['background']
                character_dict['intro'] = character['intro']
                character_dict['appearance'] = character['appearance']
                character_dict['traits'] = character['traits']
                character_dict['tone'] = character['tone']
                character_dict['response_emojis'] = character['response_emojis']
                character_dict['response_gestures'] = character['response_gestures']
                if character['character_tags']:
                    character_dict['character_tags'] = character['character_tags']
                if character['opening_line']:
                    character_dict['opening_line'] = character['opening_line']
                if character['character_info']:
                    character_dict['recent_ongoing'] = character['character_info'].get('recent_ongoing', '')
                    character_dict['emotion'] = character['character_info'].get('emotion', '')
                if character['lore_list']:
                    character_dict['lore_list'] = [lore['details'] for lore in character['lore_list']]
                if character['module_details']:
                    modules = []
                    for module in character['module_details']:
                        module_dict = {
                            'name': module['name'],
                            'category': module['category'],
                            'entries': [entry.pop('entrie_id') for entry in module['entries']]
                        }
                        modules.append(module_dict)
                    character_dict['modules'] = modules
                characters.append(character_dict)
            chapter_dict['characters'] = characters

            chapters.append(chapter_dict)
        game_dict['chapters'] = chapters

        return game_dict