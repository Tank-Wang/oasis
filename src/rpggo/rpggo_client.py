import requests
import uuid
import json
import os
from dotenv import load_dotenv
from ..utils.log import get_logger

# Load environment variables
load_dotenv()

API_BASE_URL = "https://api.rpggo.ai"
AUTH_TOKEN = f"Bearer {os.getenv('RPGGO_API_TOKEN')}"

logger = get_logger('RPGGOClient')

class RPGGOClient:
    """RPGGO API Client"""
    
    def __init__(self):
        self.api_base_url = API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': AUTH_TOKEN
        })
        self.session_id = str(uuid.uuid4())

    def get_game_metadata(self, game_id):
        """
        Get game metadata
        
        Args:
            game_id: Game ID
            
        Returns:
            dict: Game metadata
        """
        # url = f"{self.api_base_url}/v2/open/game/gamemetadata"
        # TODO: change to the new API
        # use this api to get more detailed game metadata
        url = "https://backend-pro-qavdnvfe5a-uc.a.run.app/open/creator/game/gameData"
        
        data = {
            "game_id": game_id
        }
        
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            logger.debug(json.dumps(response.json(), indent=2, ensure_ascii=False))
            object = response.json()['data']
            if isinstance(object, list):
                return object[0]
            else:
                return object
        except Exception as e:
            logger.error(f"Error in get_game_metadata: {e}")
            return None

    def start_game(self, game_id):
        """
        Initialize game session
        
        Args:
            game_id: Game ID
            
        Returns:
            dict: Game initialization response
        """
        url = f"{self.api_base_url}/v2/open/game/startgame"
        
        data = {
            "game_id": game_id,
            "session_id": self.session_id
        }
        
        response = self.session.post(url, json=data)
        response.raise_for_status()
        logger.debug(json.dumps(response.json(), indent=4, ensure_ascii=False))
        return response.json()['data']
        
    def send_action(self, game_id, character_id, message, llm_config=None)->list:
        """
        Send player action and get response
        
        Args:
            game_id: Game ID
            character_id: Character ID
            message: Player's message content
            llm_config: LLM configuration
        Returns:
            dict: Parsed NPC response
        """
        if not game_id or not character_id or not message:
            logger.error("game_id, character_id, or message is empty")
            return None

        url = f"{self.api_base_url}/v2/open/game/chatsse"
        if llm_config is None:
            chat_llm_config = {
                "chat_model": "gpt-4o",
                "temperature": 0.8
            }
        else:
            chat_llm_config = llm_config.copy()

        data = {
            "game_id": game_id,
            "session_id": self.session_id,
            "character_id": character_id,
            "message_id": str(uuid.uuid4())[:10],
            "message": message,
            "llm_config": chat_llm_config,
            "advance_config": {
                "enable_async_npc_streaming": True,
                "enable_image_streaming": False,
                "enable_voice_streaming": False
            }
        }

        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            
            # Parse response data
            raw_messages = response.text
            logger.debug(f"Received raw response: {raw_messages}")
            
            messages = raw_messages.split('\n')
            return_msg = []
            for message in messages:
                if message.startswith('data:'):
                    # Extract JSON string
                    json_start = message.find('{')
                    json_end = message.rfind('}') + 1
                    if json_start != -1 and json_end != -1:
                        json_str = message[json_start:json_end]
                        try:
                            json_obj = json.loads(json_str)
                            return_msg.append(json_obj['data'])
                        except json.JSONDecodeError:
                            logger.error(f"Error in decode message: {message}")
                            continue
                            
            return return_msg
            
        except Exception as e:
            logger.error(f"Error in send_action: {e}")
            return None

if __name__ == "__main__":
    client = RPGGOClient()
    client.get_game_metadata("ad096c5c-8420-4f85-b7bd-71104d7668da")
    client.get_game_metadata("GAAISMK3O")
    client.start_game("CB4JIETSR")
    print(client.send_action("CB4JIETSR", "CB4JIETSR", "hi"))