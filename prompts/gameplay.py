from configs.settings import Settings

settings = Settings()

AI_PLAYER_SYSTEM_PROMPT = "You are an online player for a web based game"

DATA_LOCKDOWN_PROMPT = f""""
STEP 1: Go to {settings.URI}

STEP 2: Wait for human in the loop to signin for 10 seconds

STEP 3: Navigate to the games page by clicking on the 'Games' option on the sidebar

STEP 4: Navigate to the data lockdown game by clicking on 'Data Lockdown'

STEP 5: Click on 'Start Solo' to launch the game

STEP 6: Click 'Launch Game'

STEP 7: The game will show up in a iframe in the center, click on the 'START SHIFT' button to actually start the game

STEP 8: Wait for 10 seconds for the game to load 

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