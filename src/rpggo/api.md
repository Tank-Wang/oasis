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
```json
  {
    "code": 0,
    "msg": "ok",
    "data": {
        "name": "📒 BAC -Break the boundaries",
        "game_id": "42d029a8-b5a7-49cb-94f4-8baefb0b898a",
        "background": "",
        "intro": "In 2102, Terminus City has clear class divides, with Mega Corporation ruling. Rebels in the Wild Hope District challenge this after a drone crash.",
        "image": "https://storage.googleapis.com/rpggo-game/rpggo-creator/5c642a81-e09a-4349-b3a2-f00156479dff/9cc4b0a4-6bfa-489a-aee8-57217a2c5cfd",
        "genre": "published",
        "user_id": "",
        "moderation_level": "",
        "background_musics": null,
        "chapters": [
            {
                "name": "The Crash",
                "chapter_id": "da08c8ff-490e-4a7f-853c-c64d8c803b15",
                "background": "Prologue - Marco (you,Player), an underground street racer from the Wild Hope District, is born with a restless nature flowing in his blood, and his sister Chiara seems equally rebellious under his influence.\n\nChiara connected her consciousness to a drone and infiltrated Terminus, but unfortunately, the drone crashed midway. The accident caused severe neurological trauma to Chiara, and angry Marco swore to find the culprit.\n\nhint:\n(Ask each character who they are)\n(Ask each character what happened before and after the accident)\n(Ask each character if they helped Chiara)\n(Ask each character the cause of the accident)",
                "intro": "None",
                "image": "",
                "background_audio": "",
                "ending_audio": ""
            }
        ],
        "interaction": null,
        "created_at": "2024-03-13T04:53:43Z",
        "updated_at": "2024-04-25T04:41:56Z"
    }
}
```
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

#### Sample Request
```bash
curl --location 'https://api.rpggo.ai/v2/open/game/startgame' \
--header 'accept: application/json' \
--header '' \
--header 'Content-Type: application/json' \
--data '{
  "game_id": "42d029a8-b5a7-49cb-94f4-8baefb0b898a",
  "session_id": "42d029a8sdrrwqd"
}'
```


#### Response Codes
- 200: OK
```json
{
    "code": 0,
    "msg": "ok",
    "data": {
        "name": "📒 BAC -Break the boundaries",
        "game_id": "42d029a8-b5a7-49cb-94f4-8baefb0b898a",
        "background": "",
        "intro": "In 2102, Terminus City has clear class divides, with Mega Corporation ruling. Rebels in the Wild Hope District challenge this after a drone crash.",
        "image": "https://storage.googleapis.com/rpggo-game/rpggo-creator/5c642a81-e09a-4349-b3a2-f00156479dff/9cc4b0a4-6bfa-489a-aee8-57217a2c5cfd",
        "genre": "published",
        "user_id": "ed10dbe4-7b90-46b8-9d8c-49acbca791ee",
        "chapter": {
            "name": "The Crash",
            "chapter_id": "da08c8ff-490e-4a7f-853c-c64d8c803b15",
            "background": "Prologue - Marco (you,Player), an underground street racer from the Wild Hope District, is born with a restless nature flowing in his blood, and his sister Chiara seems equally rebellious under his influence.\n\nChiara connected her consciousness to a drone and infiltrated Terminus, but unfortunately, the drone crashed midway. The accident caused severe neurological trauma to Chiara, and angry Marco swore to find the culprit.\n\nhint:\n(Ask each character who they are)\n(Ask each character what happened before and after the accident)\n(Ask each character if they helped Chiara)\n(Ask each character the cause of the accident)",
            "intro": "None",
            "image": "",
            "background_audio": "",
            "ending_audio": "",
            "characters": [
                {
                    "id": "7ed2dfa5-bcbc-4621-b2bd-dc0d0555811e",
                    "name": "Chiara",
                    "type": "dm",
                    "avatar": "https://storage.googleapis.com/rpggo-game/rpggo-creator/24fd170e-5116-41c8-8d93-57b148d50e42/6bb48ef3-9da7-4e6b-88a6-cc297a0e2987",
                    "phases": [
                        "default"
                    ]
                },
                {
                    "id": "ea1858ce-5317-4689-b940-742dbe0919c8",
                    "name": "Luca",
                    "type": "npc",
                    "avatar": "https://storage.googleapis.com/rpggo-game/rpggo-creator/c47caf17-2a05-44c5-a494-47683b40aef3/f38a1fea-d364-4ee0-b7d7-fb45d9c42593",
                    "phases": [
                        "default"
                    ]
                },
                {
                    "id": "cb3059a6-3fba-4dc9-a1b0-f20e6bb4e9ec",
                    "name": "Alessio",
                    "type": "npc",
                    "avatar": "https://storage.googleapis.com/rpggo-game/rpggo-creator/f73cd10c-23a0-4dc2-88ad-9663d3b54c1d/7b8842a0-13d7-4668-a268-67d6eb1099df",
                    "phases": [
                        "default"
                    ]
                },
                {
                    "id": "6032b7f2-b514-409e-9a65-bcceb975daa8",
                    "name": "Giulia",
                    "type": "npc",
                    "avatar": "https://storage.googleapis.com/rpggo-game/rpggo-creator/fe88083b-6221-4550-9dc9-8f5cbb395946/ce26fd17-e78e-4ded-94f8-0b0f29c33d8e",
                    "phases": [
                        "default"
                    ]
                },
                {
                    "id": "4a5a365f-23ac-443e-9f3d-0ca59b913d15",
                    "name": "Francesca",
                    "type": "npc",
                    "avatar": "https://storage.googleapis.com/rpggo-game/rpggo-creator/f7cbf80b-7f3f-4b7b-9e23-587d07135f67/fde545d3-a3ec-48d6-810f-b6e90bcf0b92",
                    "phases": [
                        "default"
                    ]
                }
            ]
        },
        "created_at": "2024-03-13T04:53:43Z",
        "updated_at": "2024-04-25T04:41:56Z"
    }
}
```

### 3. Switch Chapter
Switch the current chapter to another chapter.

`POST https://api.rpggo.ai/v2/open/game/changechapter`

#### Request Body Parameters
| Name | Type | Description |
|------|------|-------------|
| game_id | String | The unique id of the game |
| chapter_id | String | The unique id of the target chapter |
| session_id | String | The unique id to identify the play session |

#### Sample Request
```bash
curl --location 'https://api.rpggo.ai/v2/open/game/changechapter' \
--header 'accept: application/json' \
--header '' \
--header 'Content-Type: application/json' \
--data '{
  "game_id": "42d029a8-b5a7-49cb-94f4-8baefb0b898a",
  "chapter_id": "da08c8ff-490e-4a7f-853c-c64d8c803b15",
  "session_id": "42d029a8sdrrwqd"
}'
```

#### Response Codes
- 200: OK
```json
{
    "code": 0,
    "msg": "ok",
    "data": {
        "name": "📒 BAC -Break the boundaries",
        "game_id": "42d029a8-b5a7-49cb-94f4-8baefb0b898a",
        "background": "",
        "intro": "In 2102, Terminus City has clear class divides, with Mega Corporation ruling. Rebels in the Wild Hope District challenge this after a drone crash.",
        "image": "https://storage.googleapis.com/rpggo-game/rpggo-creator/5c642a81-e09a-4349-b3a2-f00156479dff/9cc4b0a4-6bfa-489a-aee8-57217a2c5cfd",
        "genre": "published",
        "user_id": "ed10dbe4-7b90-46b8-9d8c-49acbca791ee",
        "chapter": {
            "name": "The Crash",
            "chapter_id": "da08c8ff-490e-4a7f-853c-c64d8c803b15",
            "background": "Prologue - Marco (you,Player), an underground street racer from the Wild Hope District, is born with a restless nature flowing in his blood, and his sister Chiara seems equally rebellious under his influence.\n\nChiara connected her consciousness to a drone and infiltrated Terminus, but unfortunately, the drone crashed midway. The accident caused severe neurological trauma to Chiara, and angry Marco swore to find the culprit.\n\nhint:\n(Ask each character who they are)\n(Ask each character what happened before and after the accident)\n(Ask each character if they helped Chiara)\n(Ask each character the cause of the accident)",
            "intro": "None",
            "image": "",
            "background_audio": "",
            "ending_audio": "",
            "background_musics": null,
            "characters": [
                {
                    "id": "7ed2dfa5-bcbc-4621-b2bd-dc0d0555811e",
                    "name": "Chiara",
                    "type": "dm",
                    "avatar": "https://storage.googleapis.com/rpggo-game/rpggo-creator/24fd170e-5116-41c8-8d93-57b148d50e42/6bb48ef3-9da7-4e6b-88a6-cc297a0e2987",
                    "phases": [
                        "default"
                    ]
                },
                {
                    "id": "ea1858ce-5317-4689-b940-742dbe0919c8",
                    "name": "Luca",
                    "type": "npc",
                    "avatar": "https://storage.googleapis.com/rpggo-game/rpggo-creator/c47caf17-2a05-44c5-a494-47683b40aef3/f38a1fea-d364-4ee0-b7d7-fb45d9c42593",
                    "phases": [
                        "default"
                    ]
                },
                {
                    "id": "cb3059a6-3fba-4dc9-a1b0-f20e6bb4e9ec",
                    "name": "Alessio",
                    "type": "npc",
                    "avatar": "https://storage.googleapis.com/rpggo-game/rpggo-creator/f73cd10c-23a0-4dc2-88ad-9663d3b54c1d/7b8842a0-13d7-4668-a268-67d6eb1099df",
                    "phases": [
                        "default"
                    ]
                },
                {
                    "id": "6032b7f2-b514-409e-9a65-bcceb975daa8",
                    "name": "Giulia",
                    "type": "npc",
                    "avatar": "https://storage.googleapis.com/rpggo-game/rpggo-creator/fe88083b-6221-4550-9dc9-8f5cbb395946/ce26fd17-e78e-4ded-94f8-0b0f29c33d8e",
                    "phases": [
                        "default"
                    ]
                },
                {
                    "id": "4a5a365f-23ac-443e-9f3d-0ca59b913d15",
                    "name": "Francesca",
                    "type": "npc",
                    "avatar": "https://storage.googleapis.com/rpggo-game/rpggo-creator/f7cbf80b-7f3f-4b7b-9e23-587d07135f67/fde545d3-a3ec-48d6-810f-b6e90bcf0b92",
                    "phases": [
                        "default"
                    ]
                }
            ]
        },
        "created_at": "2024-03-13T04:53:43Z",
        "updated_at": "2024-04-25T04:41:56Z"
    }
}
```

### 4. Resume Game Session
Continue playing from a previous session.

`POST https://api.rpggo.ai/v2/open/game/resumesession`

#### Request Body Parameters
| Name | Type | Description |
|------|------|-------------|
| game_id | String | The unique id of the game |
| session_id | String | The unique id to identify the play session |

#### Sample Request
```bash
curl --location 'https://api.rpggo.ai/v2/open/game/resumesession' \
--header 'accept: application/json' \
--header 'Authorization: ' \
--header 'Content-Type: application/json' \
--data '{
  "game_id": "42d029a8-b5a7-49cb-94f4-8baefb0b898a",
  "session_id": "42d029a8sdrrwqd"
}'
```

#### Response Codes
- 200: OK
```json
{
    "code": 0,
    "msg": "ok",
    "data": {
        "name": "📒 BAC -Break the boundaries",
        "game_id": "42d029a8-b5a7-49cb-94f4-8baefb0b898a",
        "background": "",
        "intro": "In 2102, Terminus City has clear class divides, with Mega Corporation ruling. Rebels in the Wild Hope District challenge this after a drone crash.",
        "image": "https://storage.googleapis.com/rpggo-game/rpggo-creator/5c642a81-e09a-4349-b3a2-f00156479dff/9cc4b0a4-6bfa-489a-aee8-57217a2c5cfd",
        "genre": "published",
        "user_id": "ed10dbe4-7b90-46b8-9d8c-49acbca791ee",
        "chapter": {
            "name": "The Crash",
            "chapter_id": "da08c8ff-490e-4a7f-853c-c64d8c803b15",
            "background": "Prologue - Marco (you,Player), an underground street racer from the Wild Hope District, is born with a restless nature flowing in his blood, and his sister Chiara seems equally rebellious under his influence.\n\nChiara connected her consciousness to a drone and infiltrated Terminus, but unfortunately, the drone crashed midway. The accident caused severe neurological trauma to Chiara, and angry Marco swore to find the culprit.\n\nhint:\n(Ask each character who they are)\n(Ask each character what happened before and after the accident)\n(Ask each character if they helped Chiara)\n(Ask each character the cause of the accident)",
            "intro": "None",
            "image": "",
            "background_audio": "",
            "ending_audio": "",
            "characters": [
                {
                    "id": "7ed2dfa5-bcbc-4621-b2bd-dc0d0555811e",
                    "name": "Chiara",
                    "type": "dm",
                    "avatar": "https://storage.googleapis.com/rpggo-game/rpggo-creator/24fd170e-5116-41c8-8d93-57b148d50e42/6bb48ef3-9da7-4e6b-88a6-cc297a0e2987",
                    "phases": [
                        "default"
                    ]
                },
                {
                    "id": "ea1858ce-5317-4689-b940-742dbe0919c8",
                    "name": "Luca",
                    "type": "npc",
                    "avatar": "https://storage.googleapis.com/rpggo-game/rpggo-creator/c47caf17-2a05-44c5-a494-47683b40aef3/f38a1fea-d364-4ee0-b7d7-fb45d9c42593",
                    "phases": [
                        "default"
                    ]
                },
                {
                    "id": "cb3059a6-3fba-4dc9-a1b0-f20e6bb4e9ec",
                    "name": "Alessio",
                    "type": "npc",
                    "avatar": "https://storage.googleapis.com/rpggo-game/rpggo-creator/f73cd10c-23a0-4dc2-88ad-9663d3b54c1d/7b8842a0-13d7-4668-a268-67d6eb1099df",
                    "phases": [
                        "default"
                    ]
                },
                {
                    "id": "6032b7f2-b514-409e-9a65-bcceb975daa8",
                    "name": "Giulia",
                    "type": "npc",
                    "avatar": "https://storage.googleapis.com/rpggo-game/rpggo-creator/fe88083b-6221-4550-9dc9-8f5cbb395946/ce26fd17-e78e-4ded-94f8-0b0f29c33d8e",
                    "phases": [
                        "default"
                    ]
                },
                {
                    "id": "4a5a365f-23ac-443e-9f3d-0ca59b913d15",
                    "name": "Francesca",
                    "type": "npc",
                    "avatar": "https://storage.googleapis.com/rpggo-game/rpggo-creator/f7cbf80b-7f3f-4b7b-9e23-587d07135f67/fde545d3-a3ec-48d6-810f-b6e90bcf0b92",
                    "phases": [
                        "default"
                    ]
                }
            ]
        },
        "created_at": "2024-03-13T04:53:43Z",
        "updated_at": "2024-04-25T04:41:56Z"
    }
}
```

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

##### Normal Conversation Request
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

#### Normal Conversation Message
```json
fin
data
{"ret":200,"message":"success","data":{"result":{"character_id":"goal_check_dm","character_type":"goal_check_dm","image":"","text":"","text_ext":"","epoch":{"current_count":0,"max_chat_count":0},"insiders":[],"message_id":"b5fasdffxef"},"game_status":{"game_id":"42d029a8-b5a7-49cb-94f4-8baefb0b898a","goal_id":"","goal":{"chapter_tip":{"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","closing_statement":""},"goals_status":[]},"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","action":0,"action_message":"","game_meta":{"shared_memory":{"goal_check_dm_epoch":1}},"chapters_map":["da08c8ff-490e-4a7f-853c-c64d8c803b15"]}}}
data
{"ret":200,"message":"success","data":{"result":{"character_id":"7ed2dfa5-bcbc-4621-b2bd-dc0d0555811e","character_type":"common_npc","image":"","text":"Hey there! *(smiling)* What's up? 😊","text_ext":"","epoch":{"current_count":1,"max_chat_count":90},"insiders":["7ed2dfa5-bcbc-4621-b2bd-dc0d0555811e","ea1858ce-5317-4689-b940-742dbe0919c8","cb3059a6-3fba-4dc9-a1b0-f20e6bb4e9ec","6032b7f2-b514-409e-9a65-bcceb975daa8","4a5a365f-23ac-443e-9f3d-0ca59b913d15"],"message_id":"b5fasdffxef"},"game_status":{"game_id":"42d029a8-b5a7-49cb-94f4-8baefb0b898a","goal_id":"goals0","goal":{"chapter_tip":{"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","closing_statement":""},"goals_status":[]},"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","action":0,"action_message":"","game_meta":{},"chapters_map":[]}}}
```

##### Multimodal Conversation Request
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

#### Multimodal Conversation Message
```json
fin
data
{"ret":200,"message":"success","data":{"result":{"character_id":"picture_produce_dm","character_type":"picture_produce_dm","image":"https://storage.googleapis.com/rpggo-imagegen/42d029a8-b5a7-49cb-94f4-8baefb0b898a/f28452f5a91b4ce687d56c0c08cd454f.jpeg","image_type":1,"text":"With a spark of excitement in her eyes, Chiara leans in, recounting her close encounter—a shadowy figure adorned with a familiar emblem, hinting at connections to the racing underworld.","text_ext":"","epoch":{"current_count":0,"max_chat_count":0},"insiders":[],"message_id":"lkxQ8yGzbklVp3DwlHWQH","log_id":"10077ae2-637b-4558-979e-ceb3880fbb46","action_list":[]},"game_status":{"game_id":"42d029a8-b5a7-49cb-94f4-8baefb0b898a","goal_id":"","goal":{"chapter_tip":{"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","closing_statement":""},"goals_status":[]},"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","action":0,"action_message":"","game_meta":{},"chapters_map":["da08c8ff-490e-4a7f-853c-c64d8c803b15"],"displayed_status":{},"multimodal":{"action":2,"action_message":"picture produce sync"}},"transaction_details":{"ImageConsumption":{"type":"ImageConsumption","amount":4,"fund_direction":"OUT","name":"Image Streaming","description":"Create breathtaking Al-generated images that bring thegame's plot to life."}}}}
data
{"ret":200,"message":"success","data":{"result":{"character_id":"goal_check_dm","character_type":"goal_check_dm","image":"","text":"","text_ext":"","epoch":{"current_count":0,"max_chat_count":0},"insiders":[],"message_id":"b5fasdffxef"},"game_status":{"game_id":"42d029a8-b5a7-49cb-94f4-8baefb0b898a","goal_id":"","goal":{"chapter_tip":{"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","closing_statement":""},"goals_status":[]},"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","action":0,"action_message":"","game_meta":{"shared_memory":{"goal_check_dm_epoch":1}},"chapters_map":["da08c8ff-490e-4a7f-853c-c64d8c803b15"]}}}
data
{"ret":200,"message":"success","data":{"result":{"character_id":"7ed2dfa5-bcbc-4621-b2bd-dc0d0555811e","character_type":"common_npc","image":"","text":"Hey there! *(smiling)* What's up? 😊","text_ext":"","epoch":{"current_count":1,"max_chat_count":90},"insiders":["7ed2dfa5-bcbc-4621-b2bd-dc0d0555811e","ea1858ce-5317-4689-b940-742dbe0919c8","cb3059a6-3fba-4dc9-a1b0-f20e6bb4e9ec","6032b7f2-b514-409e-9a65-bcceb975daa8","4a5a365f-23ac-443e-9f3d-0ca59b913d15"],"message_id":"b5fasdffxef"},"game_status":{"game_id":"42d029a8-b5a7-49cb-94f4-8baefb0b898a","goal_id":"goals0","goal":{"chapter_tip":{"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","closing_statement":""},"goals_status":[]},"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","action":0,"action_message":"","game_meta":{},"chapters_map":[]}}}
```

### Game Control Messages

#### 1. Chapter Switch
| Character Type | Message Field | Value | Command Note |
|---------------|---------------|-------|--------------|
| goal_check_dm | data.game_status.action | 2 | Switch chapter |
| common_npc | game_status.action_message | string | The new chapter content |

```json
fin
data
{"ret":200,"message":"success","data":{"result":{"character_id":"goal_check_dm","character_type":"goal_check_dm","image":"","text":"","text_ext":"","epoch":{"current_count":0,"max_chat_count":0},"insiders":[],"message_id":"b5fasdffxef"},"game_status":{"game_id":"42d029a8-b5a7-49cb-94f4-8baefb0b898a","goal_id":"","goal":{"chapter_tip":{"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","closing_statement":""},"goals_status":[]},"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","action":2,"action_message":"","game_meta":{"shared_memory":{"goal_check_dm_epoch":1}},"chapters_map":["da08c8ff-490e-4a7f-853c-c64d8c803b15"]}}}
data
{"ret":200,"message":"success","data":{"result":{"character_id":"7ed2dfa5-bcbc-4621-b2bd-dc0d0555811e","character_type":"common_npc","image":"","text":"Hey there! *(smiling)* What's up? 😊","text_ext":"","epoch":{"current_count":1,"max_chat_count":90},"insiders":["7ed2dfa5-bcbc-4621-b2bd-dc0d0555811e","ea1858ce-5317-4689-b940-742dbe0919c8","cb3059a6-3fba-4dc9-a1b0-f20e6bb4e9ec","6032b7f2-b514-409e-9a65-bcceb975daa8","4a5a365f-23ac-443e-9f3d-0ca59b913d15"],"message_id":"b5fasdffxef"},"game_status":{"game_id":"42d029a8-b5a7-49cb-94f4-8baefb0b898a","goal_id":"goals0","goal":{"chapter_tip":{"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","closing_statement":""},"goals_status":[]},"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","action":0,"action_message":"","game_meta":{},"chapters_map":[]}}}
```

#### 2. Game Ending
| Character Type | Message Field | Value | Command Note |
|---------------|---------------|-------|--------------|
| goal_check_dm | data.game_status.action | 3 | Game is ending |
| common_npc | game_status.action_message | string | The ending summary |

```json
fin
data
{"ret":200,"message":"success","data":{"result":{"character_id":"goal_check_dm","character_type":"goal_check_dm","image":"","text":"","text_ext":"","epoch":{"current_count":0,"max_chat_count":0},"insiders":[],"message_id":"b5fasdffxef"},"game_status":{"game_id":"42d029a8-b5a7-49cb-94f4-8baefb0b898a","goal_id":"","goal":{"chapter_tip":{"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","closing_statement":""},"goals_status":[]},"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","action":3,"action_message":"","game_meta":{"shared_memory":{"goal_check_dm_epoch":1}},"chapters_map":["da08c8ff-490e-4a7f-853c-c64d8c803b15"]}}}
data
{"ret":200,"message":"success","data":{"result":{"character_id":"7ed2dfa5-bcbc-4621-b2bd-dc0d0555811e","character_type":"common_npc","image":"","text":"Hey there! *(smiling)* What's up? 😊","text_ext":"","epoch":{"current_count":1,"max_chat_count":90},"insiders":["7ed2dfa5-bcbc-4621-b2bd-dc0d0555811e","ea1858ce-5317-4689-b940-742dbe0919c8","cb3059a6-3fba-4dc9-a1b0-f20e6bb4e9ec","6032b7f2-b514-409e-9a65-bcceb975daa8","4a5a365f-23ac-443e-9f3d-0ca59b913d15"],"message_id":"b5fasdffxef"},"game_status":{"game_id":"42d029a8-b5a7-49cb-94f4-8baefb0b898a","goal_id":"goals0","goal":{"chapter_tip":{"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","closing_statement":""},"goals_status":[]},"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","action":0,"action_message":"","game_meta":{},"chapters_map":[]}}}
```

#### 3. Failed to Pass Game
| Character Type | Message Field | Value | Command Note |
|---------------|---------------|-------|--------------|
| goal_check_dm | data.game_status.action | 4 | Fail the goal |
| common_npc | goal.chapter_tip.closing_statement | string | The ending summary of failure |

```json
fin
data
{"ret":200,"message":"success","data":{"result":{"character_id":"goal_check_dm","character_type":"goal_check_dm","image":"","text":"","text_ext":"","epoch":{"current_count":0,"max_chat_count":0},"insiders":[],"message_id":"b5fasdffxef"},"game_status":{"game_id":"42d029a8-b5a7-49cb-94f4-8baefb0b898a","goal_id":"","goal":{"chapter_tip":{"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","closing_statement":"The goal is 'zingbagaly' failed."},"goals_status":[{"goal":"The goal is 'zinbagaly' failed.","goal_id":"fail_goal","achieved":true}]},"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","action":4,"action_message":"","game_meta":{"shared_memory":{"goal_check_dm_epoch":1}},"chapters_map":["da08c8ff-490e-4a7f-853c-c64d8c803b15"]}}}
data
{"ret":200,"message":"success","data":{"result":{"character_id":"7ed2dfa5-bcbc-4621-b2bd-dc0d0555811e","character_type":"common_npc","image":"","text":"Hey there! *(smiling)* What's up? 😊","text_ext":"","epoch":{"current_count":1,"max_chat_count":90},"insiders":["7ed2dfa5-bcbc-4621-b2bd-dc0d0555811e","ea1858ce-5317-4689-b940-742dbe0919c8","cb3059a6-3fba-4dc9-a1b0-f20e6bb4e9ec","6032b7f2-b514-409e-9a65-bcceb975daa8","4a5a365f-23ac-443e-9f3d-0ca59b913d15"],"message_id":"b5fasdffxef"},"game_status":{"game_id":"42d029a8-b5a7-49cb-94f4-8baefb0b898a","goal_id":"goals0","goal":{"chapter_tip":{"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","closing_statement":""},"goals_status":[]},"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","action":0,"action_message":"","game_meta":{},"chapters_map":[]}}}
```


### Other Error Messages

```json
{
  "ret": 10000303,
  "message": "The game session has ended",
  "data": null
}
```

```json
{
  "ret": 10000307,
  "message": "Data error. Please refresh the page or restart the game",
  "data": null
}
```
