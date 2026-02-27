from configs.settings import Settings

settings = Settings()

SYSTEM_PROMPT = "You are an online player for a web based game"

SESSION_JOIN_PROMPT = f""""
STEP 1: Go to {settings.URI}

STEP 2: Wait for human in the loop to signin for 10 seconds

STEP 3: Click the 'Join' button on the top right  

STEP 4: Look for team 'Alpha' and click 'Join' again

STEP 5: Wait for 10 seconds for the game to start

STEP 6: The game will show up in a iframe in the center, click on the 'START SHIFT' button to actually start the game

STEP 7: Wait for 10 seconds for the game to load 

There will be four panels in the game iframe: 'CLASSIFICATION', 'PRIVACY', 'HANDLING', 'CAMERAS'

Report what you found and any actions taken in the following format.
- thought: what you need to do
- action: the operation you undertake
- observation: what you observed from the situation
- game_complete: whether the game is complete, if the game is complete, there will be a 'SHIFT COMPLETE' in the center of the iframe
"""

COMPLETE_QUESTION_PROMPT = """
Check the game iframe for any new questions in the 'CLASSIFICATION', 'PRIVACY', or 'HANDLING' panels.
If there's a question popup, answer it with your knowledge.
Report what you found and any actions taken.

Report what you found and any actions taken in the following format.
- thought: what you need to do
- action: the operation you undertake
- observation: what you observed from the situation
- game_complete: whether the game is complete, if the game is complete, there will be a 'SHIFT COMPLETE' in the center of the iframe
"""