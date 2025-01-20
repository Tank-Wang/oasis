# An AI-based Game Evaluation Framework

## 1. Project Background

The website rpggo.ai hosts a diverse array of text-based RPG games, all created by gaming enthusiasts. These games can be experienced using our proprietary game engine, the Zagii-Engine. This platform aims to bring a community-driven gaming experience by allowing users to craft and share their adventures.

Try it out here 👉: https://rpggo.ai

![image](https://github.com/RPGGO-AI/oasis/blob/main/docs/images/game_lobby.png)


**We are looking to** develop an AI-based Game Evaluator with the primary objectives of:
- Creating an automated evaluation tool to ensure quality and consistency when the Zagii-Engine undergoes upgrades.
- Performing routine evaluations of games on the website to identify exceptional or underwhelming games, thus aiding operational staff in their development follow-ups, and potentially facilitating the creation of an AI-driven recommendation list.

The benefits of the AI Game Evaluator extend beyond these objectives, including:
- The potential for the AI Game Evaluator to evolve into a game player's assistant or copilot, helping players to better navigate and explore games.
- Serving as a rapid testing tool for creators during the Game Creation phase, providing quick evaluation results or further modification suggestions, potentially forming an essential foundation for a Creator Copilot.

## 2. Project Requirements

The AI Game Evaluator should be capable of assessing any game on rpggo and providing optimization suggestions.

### We provide the following API interface:
- An API interface to retrieve essential game information, aiding the evaluator in understanding the game's foundational setup.
  - This interface can access all the information visible to a game player, as illustrated in the image below:
    ![image](https://github.com/RPGGO-AI/oasis/blob/main/docs/images/game_meta.PNG)
- A Game Management API interface
  - Provides functions such as starting a game or switching chapters to control game progression.
- A Game Dialogue API interface
  - Serves as an API allowing players to converse with any NPC within the game, enabling the Game Evaluator to simulate a player's gameplay experience.
  - This interface also provides notifications for any changes in the game state.

**Detailed API information**: https://developer.rpggo.ai/dev-docs/player-api/api-overview/api-v2-new

### Required Implementation:
- Develop an AI-based Game Player that interacts with NPCs according to the game settings and rules for several rounds, resulting in a comprehensive game interaction session.
- Utilize AI models to automatically evaluate this interaction session, rate the gaming experience, and highlight the game's strengths and areas for improvement.


## 3. An Open Source Implementation Plan
We offer an initial implementation plan, which may serve as an example or a baseline.

### System Framework Diagram
Here is a high-level overview of the system framework:
![image](https://github.com/RPGGO-AI/oasis/blob/main/docs/images/ai_evaluator.png)

### Code Repository
GitHub: https://github.com/RPGGO-AI/oasis

## 4. About Game Evaluation

### Evaluation Modes
We aim to support the following two evaluation modes:
- Player Perspective Evaluation
  - Evaluating the game from a player's viewpoint by playing several rounds, then providing feedback and improvement suggestions. This assists creators in optimizing their game works more efficiently.

- Model Comparison Evaluation
  - Using different dialogue models and request parameters under the same game setting to compare performance. This assists developers in assessing the impact of technical iterations.

### Evaluation Criteria

- Game Aspects
  - Focus on aspects such as:
    - Playability of the game
    - Richness of the storyline
    - Style & theme
    - ......

- NPC Characteristics
  - Focus on aspects such as:
    - Whether NPCs adhere to character settings in their role-playing
    - The impact of NPCs on advancing the game’s storyline
    - Whether NPC dialogues are cohesive and free from inappropriate language usage, repetition, etc.
    - ......
