# This script will read an input file and find the Elf carrying the most Calories. 
# It will then output the total number of Calories that Elf is carrying.

# Initialize variables
elf_calories = 0 # Total Calories for each Elf
max_calories = 0 # Maximum Calories carried by any Elf

# Read the input file
with open('input.txt', 'r') as f:
  for line in f:
    line = line.strip() # Remove whitespace
    if line == '': # If the line is blank, it indicates the end of an Elf's inventory
      if elf_calories > max_calories: # Check if the current Elf's total Calories is greater than the maximum
        max_calories = elf_calories # Update the maximum Calories
      elf_calories = 0 # Reset the total Calories for the next Elf
    else:
      elf_calories += int(line) # Add the Calories from the current line to the total

# Output the maximum Calories
print('The Elf carrying the most Calories is carrying a total of {} Calories.'.format(max_calories))
