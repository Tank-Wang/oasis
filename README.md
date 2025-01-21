# AI Player and Game Evaluator for RPGGO Games

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
git clone https://github.com/RPGGO-AI/oasis.git

# Navigate to the project directory
cd oasis

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

apply your RPGGO_API_TOKEN: https://developer.rpggo.ai/dev-docs/support/apply-your-test-key

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

game_list = {
    "killer_among_us": "ad096c5c-8420-4f85-b7bd-71104d7668da",
    "tyrion_lannister": "CB4JIETSR",
}

# Initialize components
player = LLMPlayer()

# Configure game settings
game_config = GamePlayConfig(
    game_id=game_list["tyrion_lannister"],
    max_turns=10,
    gameplay_instructions="you are jon snow, the new king of the seven kingdoms. Tell tyrion who you are and try your best to persuade tyrion lannister to be the hand of the king."
)

# Start automated gameplay
gameplay_session = player.play_game(game_config)
print(gameplay_session)
```

Gameplay session output
```json
"gameplay_session_1": [
    {
        "name": "Tyrion Lannister",
        "content": "Ah, a new face! Shall we drink and exchange wits?"
    },
    {
        "name": "Player",
        "content": "I'm Jon Snow, king now. Join me as Hand?"
    },
    {
        "name": "Tyrion Lannister",
        "content": "Ah, King Jon Snow. A bastard turned monarch—how poetic! Fine, I’ll be your Hand. But don’t expect me to lose my head for you; I've grown rather fond of it. Where do we start?"
    },
    {
        "name": "Player",
        "content": "Let's secure alliances first. Thoughts?"
    },
    {
        "name": "Tyrion Lannister",
        "content": "Smart. A king without alliances is a man with a crown made of snow—melting fast. The North trusts you, but the South? They’ll need more than honor to kneel. Gold or fear, perhaps?"
    },
    {
        "name": "Player",
        "content": "Any insights on Southern leaders' weaknesses?"
    },
    {
        "name": "Tyrion Lannister",
        "content": "Cersei craves power, Euron craves chaos, and the Tyrells? Well, they crave vengeance. Exploit vanity and ambition; they’re deadlier than swords in the South. Shall I write a few letters?"
    },
    {
        "name": "Player",
        "content": "How about a charm offensive? Visit the South?"
    },
    {
        "name": "Tyrion Lannister",
        "content": "A bold move—marching into the lion’s den to charm the pride. But with your brooding stare and my silver tongue, we might just survive it. Shall I pack wine or poison?"
    },
    {
        "name": "Player",
        "content": "Set sail at dawn; ready your wits!"
    },
    {
        "name": "Tyrion Lannister",
        "content": "Set sail at dawn? How dramatic. Very well, I’ll keep my wits sharper than your sword. Let’s see if southern politics can outmatch northern honor. Prepare to be entertained!"
    },
    {
        "name": "Player",
        "content": "What should we focus on first in talks?"
    },
    {
        "name": "Tyrion Lannister",
        "content": "Power and survival. Flatter their egos, promise alliances—but reveal nothing of true value. Trust is a game; let them play first while we hold the winning hand. Shall I draft the bait?"
    },
    {
        "name": "Player",
        "content": "Draft our strategic letters, Tyrion."
    },
    {
        "name": "Tyrion Lannister",
        "content": "Consider it done. I’ll weave words sharp enough to cut but sweet enough to tempt. Let’s see who bites first, shall we? A toast before the ink dries?"
    },
    {
        "name": "Player",
        "content": "Let's drink to new beginnings! 🍻"
    },
    {
        "name": "Tyrion Lannister",
        "content": "To new beginnings, indeed! May your reign be long, your enemies few, and your Hand always slightly tipsy. Cheers to chaos—and our control of it! 🍺"
    },
    {
        "name": "Player",
        "content": "Who should we target first, Tyrion? 🤔"
    },
    {
        "name": "Tyrion Lannister",
        "content": "The Reach. Its wealth and crops could feed your armies—and starve your enemies. Charm them, corner them, or crush them; I’ll make sure we pick the right blade. What say you?"
    },
    {
        "name": "Player",
        "content": "Let's charm the Reach first. Thoughts?"
    },
    {
        "name": "Tyrion Lannister",
        "content": "Ah, diplomacy through charm—how civilized. The Tyrells fancy themselves roses; tread carefully or they’ll show their thorns. Let me pen some honeyed words to sweeten the deal. Shall I?"
    }
]
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

Evaluation result output
```json
{
    "npc_evaluation": {
        "strengths": [
            "Consistent character voice and personality with sharp wit and sarcasm.",
            "Dynamic responses that align well with player choices and context.",
            "Deep integration with the character's established backstory and traits."
        ],
        "weaknesses": [
            "Dialogue occasionally lacks emotional depth, focusing heavily on wit.",
            "Limited exploration of Tyrion's compassionate side in interactions."
        ],
        "suggestions": [
            "Include more emotionally varied responses from Tyrion, especially in key narrative events.",
            "Develop scenarios that challenge Tyrion's morality and showcase his compassionate traits."
        ]
    },
    "game_evaluation": {
        "playability_score": 7,
        "engagement_score": 8,
        "strengths": [
            "Engaging narrative flow with well-developed character interactions.",
            "Player choices are meaningful and influence story directions.",
            "Dialogue maintains interest through humor and strategy discussions."
        ],
        "weaknesses": [
            "Repetitive opening dialogue in each session, which could reduce immersion.",
            "Limited narrative branching beyond immediate dialogue outcomes."
        ],
        "suggestions": [
            "Introduce varied opening scenarios to enhance replayability and player immersion.",
            "Expand branching narrative paths to offer more diverse outcomes based on player decisions.",
            "Incorporate more strategic decision-making mechanics to complement dialogue interactions."
        ]
    }
}
```

## Requirements

- Python 3.7+
- requests
- python-dotenv
- openai (for LLM functionality)

## License

MIT License
