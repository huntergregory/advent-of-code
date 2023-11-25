# Read the input file
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
