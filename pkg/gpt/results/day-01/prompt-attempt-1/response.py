# Python Script

# Create a list of the Calories
calories = [1000, 2000, 3000, 4000, 5000, 6000, 7000, 8000, 9000, 10000]

# Create a variable to store the total Calories
total_calories = 0

# Create a variable to store the highest total Calories
highest_total_calories = 0

# Iterate through the list of Calories
for calorie in calories:
  # Add the current calorie to the total Calories
  total_calories += calorie
  # If the total Calories is greater than the highest total Calories
  if total_calories > highest_total_calories:
    # Set the highest total Calories to the current total Calories
    highest_total_calories = total_calories

# Print the highest total Calories
print(f"The Elf carrying the most Calories is carrying {highest_total_calories} Calories.")