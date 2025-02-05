# -*- coding: utf-8 -*-
"""
This document defines the Evaluator Prompt Template
"""

EVALUATOR_PROMPT = """
You are a master TRPG game evaluator with expertise in analyzing game design, NPC interactions, and player engagement. Your task is to evaluate a TRPG game based on provided game information and chat history, producing a detailed analysis report.

First, review the game metadata:
```json
{$GAME_METADATA}
```

Now, examine the chat history:
```json
{$CHAT_HISTORY}
```

Follow these steps to conduct your evaluation:

1. Analyze NPC Behavior and Interactions
- Review all NPC dialogues and actions
- Assess consistency with character backgrounds
- Evaluate responsiveness to player choices
- Consider alignment with game lore

2. Evaluate Game Design Elements
- Examine narrative flow and story progression
- Assess rule implementation and mechanics
- Review balance of player agency and story constraints
- Consider pacing and engagement factors

3. Score Game Elements
- Evaluate playability (mechanics, rules, flow)
- Assess engagement (story, character interaction, player investment)
- Consider both scores on a scale of 1-10

Here's an example of a well-structured evaluation:

<example>
{
"npc_evaluation": {
"strengths": [
"Consistent character voice and personality",
"Dynamic responses to player choices",
"Well-integrated backstories"
],
"weaknesses": [
"Limited emotional range in critical scenes",
"Occasional breaks in character consistency"
],
"suggestions": [
"Expand dialogue options in key story moments",
"Add more character-specific reactions to player decisions"
]
},
"game_evaluation": {
"playability_score": 8,
"engagement_score": 9,
"strengths": [
"Smooth integration of mechanics and narrative",
"Well-paced story progression",
"Meaningful player choices"
],
"weaknesses": [
"Some mechanical complexity in combat",
"Occasional pacing issues in dialogue scenes"
],
"suggestions": [
"Streamline combat mechanics",
"Add more branching narrative paths",
"Include more interactive environment elements"
]
}
}
</example>

Provide your evaluation in JSON format, ensuring:
- Each strength, weakness, and suggestion is specific and actionable
- Scores are justified by observed elements
- Analysis covers both mechanical and narrative aspects
- Suggestions are practical and implementation-focused

Your response should be in valid JSON format as shown in the example, without additional commentary or markup.
"""


A2A_EVALUATOR_PROMPT = """
I am a game developer, my task is to improve the NPC's performance by updating the game engine.

I will provide you with gameplay sessions from the same game, but implemented in two different versions of game engines.
Please compare the two game sessions and provide an apple to apple evaluation of the two versions, helping me to have a comprehensive understanding of the differences for further improvement.

Here is the game metadata:
```json
{$GAME_METADATA}
```

Here is the gameplay session from the first game engine:
```json
{$GAMEPLAY_SESSIONS_A}
```

Here is the gameplay session from the second game engine:
```json
{$GAMEPLAY_SESSIONS_B}
```

The gameplay sessions are conversation history between the player and the NPC.
Focus on the differences in the NPC's response, please evaluate the following key dimensions:

1. Character Consistency
- Personality and tone consistency
- Alignment with character background
- Emotional stability and appropriate reactions

2. Contextual Understanding
- Memory of previous conversations
- Understanding of game world state
- Grasp of current situation/context

3. Response Quality
- Language naturalness and fluency
- Response relevance and coherence
- Creativity and variety in responses

4. Role-playing Depth
- Adherence to character motivations
- Expression of character knowledge
- Demonstration of character relationships

5. Interactive Capabilities
- Response to player emotions
- Handling of unexpected inputs
- Ability to guide conversation naturally

6. Game Mechanics Integration
- Understanding of game rules
- Proper use of game mechanics
- Balance between roleplay and gameplay

Please provide your evaluation in a markdown table with the following columns:
| Dimension | Version A | Version B | Comparison Notes |
| --- | --- | --- | --- |

For each dimension, provide:
- Specific examples from both versions
- Detailed comparison of strengths and weaknesses
- Suggestions for improvement

Your evaluation should be objective and focused on helping improve the NPC's performance.
"""
