# SSE Chat (Single Chat & Group Chat, Memory Share)
To chat with different characters, the client need to start a SSE call to receive msg.

POST https://api.rpggo.ai/v2/open/game/chatsse 

# Normal Conversation Request

```
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


# Normal Conversation Response

```
fin
data
{"ret":200,"message":"success","data":{"result":{"character_id":"goal_check_dm","character_type":"goal_check_dm","image":"","text":"","text_ext":"","epoch":{"current_count":0,"max_chat_count":0},"insiders":[],"message_id":"b5fasdffxef"},"game_status":{"game_id":"42d029a8-b5a7-49cb-94f4-8baefb0b898a","goal_id":"","goal":{"chapter_tip":{"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","closing_statement":""},"goals_status":[]},"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","action":0,"action_message":"","game_meta":{"shared_memory":{"goal_check_dm_epoch":1}},"chapters_map":["da08c8ff-490e-4a7f-853c-c64d8c803b15"]}}}
data
{"ret":200,"message":"success","data":{"result":{"character_id":"7ed2dfa5-bcbc-4621-b2bd-dc0d0555811e","character_type":"common_npc","image":"","text":"Hey there! *(smiling)* What's up? 😊","text_ext":"","epoch":{"current_count":1,"max_chat_count":90},"insiders":["7ed2dfa5-bcbc-4621-b2bd-dc0d0555811e","ea1858ce-5317-4689-b940-742dbe0919c8","cb3059a6-3fba-4dc9-a1b0-f20e6bb4e9ec","6032b7f2-b514-409e-9a65-bcceb975daa8","4a5a365f-23ac-443e-9f3d-0ca59b913d15"],"message_id":"b5fasdffxef"},"game_status":{"game_id":"42d029a8-b5a7-49cb-94f4-8baefb0b898a","goal_id":"goals0","goal":{"chapter_tip":{"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","closing_statement":""},"goals_status":[]},"chapter_id":"da08c8ff-490e-4a7f-853c-c64d8c803b15","action":0,"action_message":"","game_meta":{},"chapters_map":[]}}}
```
