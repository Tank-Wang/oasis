# RPGGO API Client

A Python client library for interacting with the RPGGO API.

## Features

- Game session initialization
- NPC conversation support 
- SSE (Server-Sent Events) response handling

## Installation

```bash
pip install rpggo-client
```

## Usage

1. First create a .env file and add your API token:
   ```
   API_TOKEN=your_api_token
   ```

2. Basic usage example:
   ```python
   from rpggo.rpggo_client import RPGGOClient
   client = RPGGOClient()
   ```

   Initialize game session:
   ```python
   game_id = "YOUR_GAME_ID"
   client.start_game(game_id)
   ```

   Chat with an NPC:
   ```python
   response = client.chat_with_npc(game_id, "CHARACTER_ID", "Hello!")
   print(response)
   ```

## Requirements

- Python 3.7+
- requests
- python-dotenv

## License

MIT License