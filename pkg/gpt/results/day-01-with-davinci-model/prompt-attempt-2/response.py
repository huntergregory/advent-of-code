# Create a list to store the calories of each elf
calories = []

# Create a variable to store the total calories of each elf
total = 0

# Create a variable to store the maximum calories of all elves
max_calories = 0

# Read the input line by line
while True:
    line = input()
    # If the line is empty, it means the end of one elf's inventory
    if line == '':
        # Store the total calories of the elf
        calories.append(total)
        # Reset the total calories
        total = 0
    # If the line is not empty, add the calories to the total
    else:
        total += int(line)
    # If the line is 'END OF INPUT', it means the end of the input
    if line == 'END OF INPUT':
        break

# Find the maximum calories among all elves
for c in calories:
    if c > max_calories:
        max_calories = c

# Print the result
print('The Elf carrying the most Calories is carrying', max_calories, 'Calories.')