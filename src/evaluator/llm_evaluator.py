# -*- coding: utf-8 -*-
"""
This file is the implementation of an LLM-based game evaluator.

TODO:
- add apple-to-apple evaluation
- update evaluator prompt
"""


import json
from typing import List, Dict
from src.utils.llm_utils import GPT
from src.utils.log import get_logger
from src.evaluator.evaluator_prompt import EVALUATOR_PROMPT, A2A_EVALUATOR_PROMPT
from src.rpggo.rpggo_client import RPGGOClient
logger = get_logger('LLMEvaluator')

class LLMEvaluator():
    """LLM-based game evaluator implementation, focusing on evaluating NPC performance and game playability"""
    
    def __init__(self):
        pass
    
    def evaluate_game_sessions(self, game_id: str, game_sessions: List[Dict]) -> Dict:
        """
        Evaluate game sessions based on multiple game dialogues

        Args:
            game_id: Game ID
            game_sessions: List of game dialogues, each element is a complete dialogue history
            
        Returns:
            evaluation: Dictionary containing evaluation results
        """
        if not game_id:
            raise ValueError("game_id is empty")

        if not game_sessions:
            raise ValueError("game_sessions is empty")
        
        if len(game_sessions) < 3:
            logger.warning("game_sessions is less than 3, recommend to include more game_sessions")

        # get game metadata
        rpggo_client = RPGGOClient()
        game_metadata = rpggo_client.get_game_metadata(game_id)
 
        # construct evaluation prompt
        prompt = self._construct_game_evaluation_prompt(game_metadata, game_sessions)
        logger.info(f"evaluator prompt: {prompt}")
        
        # get evaluation result from LLM
        gpt = GPT(model_name="gpt-4o")
        try:
            response = gpt.generate(prompt=prompt, json_mode=True)
            evaluation = json.loads(response)
            logger.debug(f"evaluation: {json.dumps(evaluation, ensure_ascii=False, indent=4)}")
        except json.JSONDecodeError as e:
            logger.error(f"JSONDecodeError: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"Error in GPT generate: {str(e)}")
            return {}

        return evaluation
    
    def a2a_evaluation(self, game_id: str, gameplay_sessions_a: List[Dict], gameplay_sessions_b: List[Dict]) -> str:
        """
        Compare two game sessions based on their dialogue history

        Args:
            game_id: Game ID
            gameplay_sessions_a: Game dialogue history of session A
            gameplay_sessions_b: Game dialogue history of session B
            
        Returns:
            evaluation: Dictionary containing evaluation results
        """
        if not game_id:
            raise ValueError("game_id is empty")

        if not gameplay_sessions_a:
            raise ValueError("gameplay_sessions_a is empty")

        if not gameplay_sessions_b:
            raise ValueError("gameplay_sessions_b is empty")
        
        rpggo_client = RPGGOClient()
        game_metadata = rpggo_client.get_game_metadata(game_id)
        if not game_metadata:
            raise ValueError("game_metadata is empty")
        
        # construct evaluation prompt
        prompt = self._construct_a2a_evaluation_prompt(game_metadata, gameplay_sessions_a, gameplay_sessions_b)
        logger.info(f"evaluator prompt: {prompt}")

        gpt = GPT(model_name="gpt-4o")
        try:
            response = gpt.generate(prompt=prompt)
            logger.debug(f"evaluation: {response}")
        except Exception as e:
            logger.error(f"Error in GPT generate: {str(e)}")
            return ""
        
        return response

    def _construct_game_evaluation_prompt(self, game_metadata: Dict, gameplay_sessions: List[Dict]) -> str:
        """Construct evaluation prompt"""
        prompt_tpl = EVALUATOR_PROMPT
        game_metadata_for_evaluation = self._get_game_metadata_for_evaluation(game_metadata)
        logger.debug(f"game_metadata_for_evaluation: {json.dumps(game_metadata_for_evaluation, ensure_ascii=False, indent=2)}")
        prompt = prompt_tpl.replace('{$GAME_METADATA}', json.dumps(game_metadata_for_evaluation, ensure_ascii=False))
        prompt = prompt.replace('{$CHAT_HISTORY}', json.dumps(gameplay_sessions, ensure_ascii=False))
        return prompt
    
    def _construct_a2a_evaluation_prompt(self, game_metadata: Dict, gameplay_sessions_a: List[Dict], gameplay_sessions_b: List[Dict]) -> str:
        """Construct evaluation prompt"""
        prompt_tpl = A2A_EVALUATOR_PROMPT
        game_metadata_for_evaluation = self._get_game_metadata_for_evaluation(game_metadata)
        # logger.debug(f"game_metadata_for_evaluation: {json.dumps(game_metadata_for_evaluation, ensure_ascii=False, indent=2)}")
        prompt = prompt_tpl.replace('{$GAME_METADATA}', json.dumps(game_metadata_for_evaluation, ensure_ascii=False))
        prompt = prompt.replace('{$GAMEPLAY_SESSIONS_A}', json.dumps(gameplay_sessions_a, ensure_ascii=False))
        prompt = prompt.replace('{$GAMEPLAY_SESSIONS_B}', json.dumps(gameplay_sessions_b, ensure_ascii=False))
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
