Experimenting with an AI system to solve code puzzles.

## Results on 2022 Puzzles
Even the Davinci model was able to solve day 1's puzzle with a good prompt (asked it to write a Python script).

For day 2's puzzle, GPT-3.5 overfit a solution to the example, hardcoding myopic if-else statements. Tried telling GPT to rewrite the script because it was incorrect, but it produced a logically equivalent script (still incorrect).

Given these results, I doubt someone could coax one of today's model to independently devise solutions for later puzzles, which become increasingly more complex.

## Note
AI should not be used for submissions impacting leaderboards. See https://adventofcode.com/about#ai_leaderboard

## Development
Run `python -m pip install <pkg>` for these packages:
- numpy
- langchain
- openai
