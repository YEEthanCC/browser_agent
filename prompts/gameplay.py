from configs.settings import Settings

settings = Settings()

AI_PLAYER_SYSTEM_PROMPT = "You are an online player for a web based game"

DATA_LOCKDOWN_PROMPT = f""""
STEP 1: Go to {settings.URI}

STEP 2: Wait for human in the loop to signin for 10 seconds

STEP 3: Click the 'Join' button on the top right  

STEP 4: Look for team 'Alpha' and click 'Join' again

STEP 5: Wait for 10 seconds for the game to start

STEP 6: The game will show up in a iframe in the center, click on the 'START SHIFT' button to actually start the game

STEP 7: Wait for 10 seconds for the game to load 

There will be four panels in the game iframe: 'CLASSIFICATION', 'PRIVACY', 'HANDLING', 'CAMERAS'

IMPORTANT: Questions will pop up randomly and continuously on 'CLASSIFICATION', 'PRIVACY', 'HANDLING' panels.

You MUST keep monitoring and answering questions until the game ends or you are told to stop.
After answering each question, immediately check for new questions.
DO NOT stop after answering just one question - this is a continuous game.

Keep playing by repeatedly:
1. Checking all panels for new question popups
2. Answering any visible questions
3. Waiting 2-3 seconds
4. Repeating the check

"""