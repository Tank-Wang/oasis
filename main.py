import json
from src.rpggo.rpggo_client import RPGGOClient
from src.player.llm_player import LLMPlayer

game_list = {
    "killer_among_us": "ad096c5c-8420-4f85-b7bd-71104d7668da",
    "tyrion_lannister": "CB4JIETSR",
}
def main():
    player = LLMPlayer()
    player.play_game(game_list["killer_among_us"])

if __name__ == "__main__":
    main() 