# RPGGO API Client

这是一个用于与RPGGO API交互的Python客户端库。

## 功能特性

- 支持游戏会话初始化
- 支持与NPC对话
- 处理SSE(Server-Sent Events)响应

## 安装

```bash
pip install rpggo-client
```

## 使用方法

1. 首先创建一个.env文件，并添加你的API令牌：
   ```
   API_TOKEN=your_api_token
   ```

2. 基本使用示例：
   ```python
   from rpggo.rpggo_client import RPGGOClient
   client = RPGGOClient()
   ```

   初始化游戏会话
   ```python
   game_id = "YOUR_GAME_ID"
   client.start_game(game_id)
   ```

   与NPC对话
   ```python
   response = client.chat_with_npc(game_id, "CHARACTER_ID", "Hello!")
   print(response)
   ```

## 环境要求

- Python 3.7+
- requests
- python-dotenv

## 许可证

MIT License