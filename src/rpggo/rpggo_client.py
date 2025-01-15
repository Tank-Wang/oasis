import requests
import uuid
import json
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

API_BASE_URL = "https://api.rpggo.ai"
AUTH_TOKEN = f"Bearer {os.getenv('RPGGO_API_TOKEN')}"

class RPGGOClient:
    """RPGGO API 客户端"""
    
    def __init__(self):
        self.api_base_url = API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': AUTH_TOKEN
        })
        self.session_id = str(uuid.uuid4())
        
    def start_game(self, game_id):
        """
        初始化游戏会话
        
        Args:
            game_id: 游戏ID
            
        Returns:
            dict: 游戏初始化响应
        """
        url = f"{self.api_base_url}/v2/open/game/startgame"
        
        data = {
            "game_id": game_id,
            "session_id": self.session_id
        }
        
        response = self.session.post(url, json=data)
        response.raise_for_status()
        # print(json.dumps(response.json(), indent=4, ensure_ascii=False))
        return response.json()
        
    def chat_with_npc(self, game_id, character_id, message):
        """
        发送玩家行动并获取响应
        
        Args:
            game_id: 游戏ID
            character_id: 角色ID
            message: 玩家的消息内容
            
        Returns:
            dict: 解析后的NPC响应
        """
        url = f"{self.api_base_url}/v2/open/game/chatsse"

        data = {
            "game_id": game_id,
            "session_id": self.session_id,
            "character_id": character_id,
            "message_id": str(uuid.uuid4())[:10],
            "message": message
        }
        
        try:
            response = self.session.post(url, json=data)
            response.raise_for_status()
            
            # 解析响应数据
            raw_messages = response.text
            messages = raw_messages.split('\n')
            
            for message in messages:
                if message.startswith('data:'):
                    # 提取JSON字符串
                    json_start = message.find('{')
                    json_end = message.rfind('}') + 1
                    if json_start != -1 and json_end != -1:
                        json_str = message[json_start:json_end]
                        try:
                            json_obj = json.loads(json_str)
                            # 检查是否为NPC响应
                            if json_obj.get('data', {}).get('result', {}).get('character_type') == 'common_npc':
                                return json_obj['data']['result']
                        except json.JSONDecodeError:
                            continue
                            
            return {"text": "No NPC response"}
            
        except Exception as e:
            print(f"Error: {e}")
            return None

if __name__ == "__main__":
    client = RPGGOClient()
    client.start_game("CB4JIETSR")
    print(client.chat_with_npc("CB4JIETSR", "CB4JIETSR", "hi"))
