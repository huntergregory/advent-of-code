## dependencies
import os

from langchain.llms import OpenAIChat
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
# from langchain.memory import ConversationBufferMemory
# from langchain.utilities import WikipediaAPIWrapper

from api.apikey import apikey
os.environ['OPENAI_API_KEY'] = apikey

TEMPERATURE = 0.3

PUZZLE_PROMPT = """Please respond with a Python script to solve the problem below. Your response should only include a compilable Python script. In this script, include comments explaining your thought process. Consider the puzzle below, which has a character-sensitive input file (that is, spaces and new lines are important in the input).


PUZZLE:
{puzzle}


SCRIPT (solving the PUZZLE based on an INPUT FILE):
"""

SCRIPT_REWRITE_PROMPT = """Please rewrite the Python script below so that it solves the problem below. Your response should only include a compilable Python script. In this script, include comments explaining your thought process. The puzzle below has a character-sensitive input file (that is, spaces and new lines are important in the input).


PUZZLE:
{puzzle}


PREVIOUS SCRIPT (this solution was overfitted to the example INPUT):
{script}


REWRITTEN SCRIPT (this time, do not overfit the solution):
"""

# TODO manually evaluating correctness for now
# EVALUATE_AND_REWRITE_PROMPT = """You already wrote a Python script. The script is meant to solve the puzzle below, which has a character-sensitive input file (that is, spaces and new lines are important in the input).

# PUZZLE:
# {puzzle}

# OUTPUT (from running your script): {output}

PUZZLE = """Rock Paper Scissors is a game between two players. Each game contains many rounds; in each round, the players each simultaneously choose one of Rock, Paper, or Scissors using a hand shape. Then, a winner for that round is selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock. If both players choose the same shape, the round instead ends in a draw.

Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) that they say will be sure to help you win. "The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.

The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors. Winning every time would be suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score. Your total score is the sum of your scores for each round. The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you, you should calculate the score you would get if you were to follow the strategy guide.

For example, suppose you were given the following strategy guide:

BEGINNING OF INPUT FILE
A Y
B X
C Z
END OF INPUT FILE

This strategy guide predicts and recommends the following:

In the first round, your opponent will choose Rock (A), and you should choose Paper (Y). This ends in a win for you with a score of 8 (2 because you chose Paper + 6 because you won).
In the second round, your opponent will choose Paper (B), and you should choose Rock (X). This ends in a loss for you with a score of 1 (1 + 0).
The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.
In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

What would your total score be if everything goes exactly according to your strategy guide?"""

SCRIPT="""# Read the input file
with open('input.txt', 'r') as file:
    lines = file.readlines()

# Initialize the total score
total_score = 0

# Iterate through each line in the input file
for line in lines:
    # Split the line into opponent's move and recommended move
    opponent_move, recommended_move = line.strip().split()

    # Determine the score for the round based on the moves
    if opponent_move == 'A' and recommended_move == 'Y':
        score = 8
    elif opponent_move == 'B' and recommended_move == 'X':
        score = 1
    elif opponent_move == 'C' and recommended_move == 'Z':
        score = 6
    else:
        score = 0

    # Add the score to the total score
    total_score += score

# Print the total score
print(total_score)
"""

# llm = OpenAI(temperature=TEMPERATURE, model_name='gpt-3.5-turbo-16k')
llm = OpenAIChat(model_name='gpt-3.5-turbo-16k', temperature = TEMPERATURE) # max_tokens=
print(llm)

# template = PromptTemplate(input_variables=['puzzle'], template=PUZZLE_PROMPT)
# chain = LLMChain(llm=llm, prompt=template, verbose=True)
# print('asking first prompt...')
# result = chain.run(puzzle=PUZZLE)
# print(result)

template = PromptTemplate(input_variables=['puzzle', 'script'], template=SCRIPT_REWRITE_PROMPT)
chain = LLMChain(llm=llm, prompt=template, verbose=True)
print('asking rewrite prompt...')
result = chain.run(puzzle=PUZZLE, script=SCRIPT)

print(result)
