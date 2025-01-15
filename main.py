import json
from src.rpggo.rpggo_client import RPGGOClient

def main():
    client = RPGGOClient()
    client.start_game("CB4JIETSR")
    print(json.dumps(client.chat_with_npc("CB4JIETSR", "CB4JIETSR", "hi"), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main() 