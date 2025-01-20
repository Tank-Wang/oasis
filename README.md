# RPGGO API Client & LLM Integration

A Python client library for interacting with RPGGO API, featuring LLM-powered player agents and gameplay evaluation capabilities.

## Key Features

- RPGGO API Client Integration
  - Game session initialization
  - NPC conversation support
  - SSE (Server-Sent Events) response handling

- LLM-Powered Player Agent
  - Automated gameplay interactions
  - Intelligent dialogue decisions
  - Context-aware behavior generation

- Gameplay Evaluation System
  - Session analysis
  - Player performance assessment
  - Improvement suggestions

## Installation

```bash
# Clone the repository
git clone https://github.com/RPGGO-AI/Oasis.git

# Navigate to the project directory
cd Oasis

# Install dependencies
pip install -r requirements.txt
```

## Usage Guide

### 1. Environment Setup

Create a .env file and add your API tokens:
```
RPGGO_API_TOKEN=your_rpggo_token
OPENAI_API_KEY=your_openai_token
```

### 2. Basic RPGGO Client Usage

```python
from src.rpggo.rpggo_client import RPGGOClient

# Initialize client
client = RPGGOClient()

# Start game session
game_id = "YOUR_GAME_ID"
client.start_game(game_id)

# Chat with NPC
response = client.send_action(game_id, "CHARACTER_ID", "Hello!")
print(response)
```

### 3. LLM Player Agent

```python
from src.player.llm_player import LLMPlayer, GamePlayConfig

# Initialize components
player = LLMPlayer()

# Configure game settings
game_config = GamePlayConfig(
    game_id="YOUR_GAME_ID",
    max_turns=10,
    gameplay_instructions="your instructions here"
)

# Start automated gameplay
gameplay_session = player.play_game(game_config)
print(gameplay_session)
```

### 4. Gameplay Evaluation

```python
from evaluator.llm_evaluator import LLMEvaluator

# Initialize components
evaluator = LLMEvaluator()
game_sessions = [gameplay_session]

# Evaluate gameplay
evaluation_result = evaluator.evaluate_game_sessions(game_id, game_sessions)
print(json.dumps(evaluation_result, ensure_ascii=False, indent=2))
```

## Requirements

- Python 3.7+
- requests
- python-dotenv
- openai (for LLM functionality)

## License

MIT License