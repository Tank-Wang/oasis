import json
from src.rpggo.rpggo_client import RPGGOClient
from src.player.llm_player import LLMPlayer

def main():
    player = LLMPlayer()
    player.play_game("CB4JIETSR")

if __name__ == "__main__":
    main() 