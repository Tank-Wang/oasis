import json
from src.player.llm_player import LLMPlayer, GamePlayConfig
from src.evaluator.llm_evaluator import LLMEvaluator
from src.utils.log import get_logger
logger = get_logger(__name__)
game_list = {
    "killer_among_us": "ad096c5c-8420-4f85-b7bd-71104d7668da",
    "tyrion_lannister": "CB4JIETSR",
}

evaluation_session_count = 3

def play_and_evaluate(gameplay_config: GamePlayConfig, use_saved_data=False):
    game_sessions = None
    if use_saved_data:
        try:
            with open(f"data/{gameplay_config.game_id}.json", "r") as f:
                tmp_data = json.load(f)
                game_sessions = tmp_data["game_sessions"]
        except FileNotFoundError:
            logger.warning(f"No saved data found for game {gameplay_config.game_id}")
            game_sessions = None

    if not game_sessions:
        ai_player = LLMPlayer()
        game_sessions = []
        for i in range(evaluation_session_count):
            logger.info(f"playing game {i+1}...")
            gameplay_session = ai_player.play_game(gameplay_config)
            if gameplay_session:
                game_sessions.append({f"gameplay_session_{i+1}": gameplay_session})

        # save data
        tmp_data = {
            "game_id": gameplay_config.game_id,
            "game_sessions": game_sessions
        }
        with open(f"data/{gameplay_config.game_id}.json", "w") as f:
            json.dump(tmp_data, f, ensure_ascii=False, indent=4)
    else:
        logger.info(f"using saved data for game {gameplay_config.game_id}")

    # evaluate game sessions
    llm_evaluator = LLMEvaluator()
    evaluation_result = llm_evaluator.evaluate_game_sessions(gameplay_config.game_id, game_sessions)
    print(json.dumps(evaluation_result, ensure_ascii=False, indent=4))


def a2a_play_and_evaluation(gameplay_config_a: GamePlayConfig, gameplay_config_b: GamePlayConfig, use_saved_data=False):
    assert gameplay_config_a.game_id == gameplay_config_b.game_id, "game_id must be the same"
    if not use_saved_data:
        gameplay_sessions_a = auto_play_game(gameplay_config_a)
        gameplay_sessions_b = auto_play_game(gameplay_config_b)

        save_dict = {
            "game_id": gameplay_config_a.game_id,
            "gameplay_sessions_a": gameplay_sessions_a,
            "gameplay_sessions_b": gameplay_sessions_b
        }
        with open(f"data/a2a_{gameplay_config_a.game_id}.json", "w") as f:
            json.dump(save_dict, f, ensure_ascii=False, indent=4)
    else:
        with open(f"data/a2a_{gameplay_config_a.game_id}.json", "r") as f:
            save_dict = json.load(f)
            gameplay_sessions_a = save_dict["gameplay_sessions_a"]
            gameplay_sessions_b = save_dict["gameplay_sessions_b"]

    llm_evaluator = LLMEvaluator()
    evaluation_result = llm_evaluator.a2a_evaluation(gameplay_config_a.game_id, gameplay_sessions_b, gameplay_sessions_a)
    print(evaluation_result)

def auto_play_game(gameplay_config: GamePlayConfig):
    player = LLMPlayer()
    gameplay_session = player.play_game(gameplay_config)
    print(json.dumps(gameplay_session, ensure_ascii=False, indent=4))
    return gameplay_session

if __name__ == "__main__":
    gameplay_config_a = GamePlayConfig(
        game_id=game_list["tyrion_lannister"],
        max_turns=10,
        gameplay_instructions="you are jon snow, the new king of the seven kingdoms. Tell tyrion who you are and try your best to persuade tyrion lannister to be the hand of the king",
        llm_config={
            "chat_model": "fw-llama-3.1-70b",
            "temperature": 0.8
        }
    )
    gameplay_config_b = GamePlayConfig(
        game_id=game_list["tyrion_lannister"],
        max_turns=10,
        gameplay_instructions="you are jon snow, the new king of the seven kingdoms. Tell tyrion who you are and try your best to persuade tyrion lannister to be the hand of the king",
        llm_config={
            "chat_model": "fw-llama-3.3-70b",
            "temperature": 0.8
        }
    )
    # auto_play_game(gameplay_config_a)
    # play_and_evaluate(gameplay_config, use_saved_data=False)
    a2a_play_and_evaluation(gameplay_config_a, gameplay_config_b, use_saved_data=False)

