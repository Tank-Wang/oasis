import json
from src.rpggo.rpggo_client import RPGGOClient
from src.player.llm_player import LLMPlayer
from src.evaluator.llm_evaluator import LLMEvaluator
from src.utils.log import get_logger

logger = get_logger(__name__)
game_list = {
    "killer_among_us": "ad096c5c-8420-4f85-b7bd-71104d7668da",
    "tyrion_lannister": "CB4JIETSR",
}

evaluation_session_count = 1

def auto_evaluation(game_id, use_saved_data=False):
    game_metadata = None
    game_sessions = None
    if use_saved_data:
        try:
            with open(f"data/{game_id}.json", "r") as f:
                tmp_data = json.load(f)
                game_metadata = tmp_data["game_metadata"]
                game_sessions = tmp_data["game_sessions"]
        except FileNotFoundError:
            logger.warning(f"No saved data found for game {game_id}")
            game_metadata = None
            game_sessions = None

    if not game_metadata or not game_sessions:
        rpggo_client = RPGGOClient()
        game_metadata = rpggo_client.get_game_metadata(game_id)
        ai_player = LLMPlayer()
        game_sessions = []
        for i in range(evaluation_session_count):
            logger.info(f"playing game {i+1}...")
            gameplay_session = ai_player.play_game(game_id)
            if gameplay_session:
                game_sessions.append({f"gameplay_session_{i+1}": gameplay_session})

        # save data
        tmp_data = {
            "game_metadata": game_metadata,
            "game_sessions": game_sessions
        }
        with open(f"data/{game_id}.json", "w") as f:
            json.dump(tmp_data, f, ensure_ascii=False, indent=4)
    else:
        logger.info(f"using saved data for game {game_id}")

    # evaluate game sessions
    llm_evaluator = LLMEvaluator()
    llm_evaluator.evaluate_game(game_metadata, game_sessions)

def auto_play_game():
    player = LLMPlayer()
    player.play_game(game_list["killer_among_us"])

if __name__ == "__main__":
    auto_evaluation(game_list["killer_among_us"], use_saved_data=True)
    # auto_play_game()
