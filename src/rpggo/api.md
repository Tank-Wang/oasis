# RPG Go API Documentation

## Game Management APIs

### 1. Get Game Metadata
Retrieve the game basic information for preview.

`POST https://api.rpggo.ai/open/game/gamelist`

#### Request Body Parameters
| Name | Type | Description |
|------|------|-------------|
| game_id | String | The unique id of the game |

#### Sample Request
```bash
curl --location 'https://api.rpggo.ai/v2/open/game/gamemetadata' \
--header 'accept: application/json' \
--header 'Authorization:' \
--header 'Content-Type: application/json' \
--data '{
  "game_id": "42d029a8-b5a7-49cb-94f4-8baefb0b898a"
}'
```

#### Response Codes
- 200: OK
- 401: Unauthorized

### 2. Start Game
Start the game at a specific chapter. If chapter_id is not specified, then start from chapter 1.

`POST https://api.rpggo.ai/v2/open/game/startgame`

#### Request Body Parameters
| Name | Type | Description |
|------|------|-------------|
| game_id | String | The unique id of the game |
| chapter_id | String | The unique id of the start chapter |
| session_id | String | The unique id to identify the play session |

### 3. Switch Chapter
Switch the current chapter to another chapter.

`POST https://api.rpggo.ai/v2/open/game/changechapter`

#### Request Body Parameters
| Name | Type | Description |
|------|------|-------------|
| game_id | String | The unique id of the game |
| chapter_id | String | The unique id of the target chapter |
| session_id | String | The unique id to identify the play session |

### 4. Resume Game Session
Continue playing from a previous session.

`POST https://api.rpggo.ai/v2/open/game/resumesession`

#### Request Body Parameters
| Name | Type | Description |
|------|------|-------------|
| game_id | String | The unique id of the game |
| session_id | String | The unique id to identify the play session |

## SSE Chat (Single Chat & Group Chat, Memory Share)

### SSE Chat Endpoint
To chat with different characters, the client needs to start a SSE call to receive messages.

#### Request Details
`POST https://api.rpggo.ai/v2/open/game/chatsse`

##### Request Body Parameters
| Name | Type | Description |
|------|------|-------------|
| game_id | String | The unique id of the game |
| session_id | String | The unique id of the game session |
| character_id | String | The unique id of the character |
| message_id | String | Any unique id to identify the message |
| message | String | The message content |
| advance_config | Dictionary | Config to enable image, voice output |

##### Headers
| Name | Type | Description |
|------|------|-------------|
| Authorization | String | Bearer Token Apply Your Test Key |
| Content-Type | String | application/json |

#### Response Types

##### 1. Normal Conversation
```bash
curl --location 'https://api.rpggo.ai/v2/open/game/chatsse' \
--header 'accept: application/json' \
--header 'Authorization: ' \
--header 'Content-Type: application/json' \
--data '{
  "character_id": "0b2d7f6b-cf8b-4bca-9aec-da8236ffb40a",
  "game_id": "42d029a8-b5a7-49cb-94f4-8baefb0b898a",
  "message": "hi",
  "message_id": "b5fasdffx",
  "session_id": "42d029a8sdrrwqd"
}'
```

##### 2. Multimodal Conversation
```bash
curl --location 'https://api.rpggo.ai/v2/open/game/chatsse' \
--header 'accept: application/json' \
--header 'Authorization: ' \
--header 'Content-Type: application/json' \
--data '{
  "game_id": "42d029a8-b5a7-49cb-94f4-8baefb0b898a",
  "character_id": "7ed2dfa5-bcbc-4621-b2bd-dc0d0555811e",
  "message": "Can you tell me more about what you saw through the drone? 📡",
  "user_id": "6bad72e7-a936-4069-84f8-670540cf3cac",
  "session_id": "2Kzoxbeht_aoHNgDeHLtN",
  "message_id": "lkxQ8yGzbklVp3DwlHWQH",
  "advance_config": {
    "enable_image_streaming": true
  }
}'
```

### Game Control Messages

#### 1. Chapter Switch
| Character Type | Message Field | Value | Command Note |
|---------------|---------------|-------|--------------|
| goal_check_dm | data.game_status.action | 2 | Switch chapter |
| common_npc | game_status.action_message | string | The new chapter content |

#### 2. Game Ending
| Character Type | Message Field | Value | Command Note |
|---------------|---------------|-------|--------------|
| goal_check_dm | data.game_status.action | 3 | Game is ending |
| common_npc | game_status.action_message | string | The ending summary |

#### 3. Failed to Pass Game
| Character Type | Message Field | Value | Command Note |
|---------------|---------------|-------|--------------|
| goal_check_dm | data.game_status.action | 4 | Fail the goal |
| common_npc | goal.chapter_tip.closing_statement | string | The ending summary of failure |

### Error Messages

#### Session Ended
```json
{
  "ret": 10000303,
  "message": "The game session has ended",
  "data": null
}
```

#### Data Error
```json
{
  "ret": 10000307,
  "message": "Data error. Please refresh the page or restart the game",
  "data": null
}
```

#### Response Codes
- 200: OK
- 401: Unauthorized