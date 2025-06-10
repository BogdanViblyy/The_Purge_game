import time
import os

# --- Game Configuration ---
# We define constants here to make it easy to change the game's balance later.

# Player's initial stats
PLAYER_INITIAL_HEALTH = 100
PLAYER_INITIAL_FOOD = 100
PLAYER_INITIAL_ENERGY = 100

# The goal: how many hours the player must survive
SURVIVAL_GOAL_HOURS = 24 

# How much resources are consumed each hour
FOOD_CONSUMPTION_PER_HOUR = 4
ENERGY_CONSUMPTION_PER_HOUR = 3

# --- Player State ---
# These variables will change during the game.
player_health = PLAYER_INITIAL_HEALTH
player_food = PLAYER_INITIAL_FOOD
player_energy = PLAYER_INITIAL_ENERGY
hours_survived = 0

# --- Main Game Loop ---
def game_loop():
    # We need to use global variables to modify them inside the function
    global player_health, player_food, player_energy, hours_survived

    print("--- THE PURGE HAS BEGUN ---")
    print(f"You must survive for {SURVIVAL_GOAL_HOURS} hours. Good luck.\n")
    time.sleep(2) # Pause for dramatic effect

    # The game continues as long as the player is alive and hasn't reached the goal
    while player_health > 0 and hours_survived < SURVIVAL_GOAL_HOURS:
        # Clear the console for a cleaner display
        os.system('cls' if os.name == 'nt' else 'clear')

        # --- Display Player Status ---
        print(f"--- Hour: {hours_survived} / {SURVIVAL_GOAL_HOURS} ---")
        print(f"Health: {player_health}%")
        print(f"Food:   {player_food}%")
        print(f"Energy: {player_energy}%")
        print("--------------------")

        # In this first version, we don't have choices yet.
        # Time simply passes.
        print("\nAnother hour passes...")

        # --- Update Game State ---
        hours_survived += 1
        player_food -= FOOD_CONSUMPTION_PER_HOUR
        player_energy -= ENERGY_CONSUMPTION_PER_HOUR

        # Check for consequences of low resources
        if player_food <= 0:
            print("You are starving! You are losing health.")
            player_health -= 5
            player_food = 0 # Prevents food from going into negative
        
        if player_energy <= 0:
            print("You are exhausted! You are losing health.")
            player_health -= 3
            player_energy = 0 # Prevents energy from going into negative

        # Prevent health from going below 0 in the display
        if player_health < 0:
            player_health = 0

        # Wait for user to press Enter to proceed to the next hour
        input("\nPress Enter to continue...")

    # --- End of Game ---
    os.system('cls' if os.name == 'nt' else 'clear')
    print("--- The night is over. ---")
    if player_health > 0:
        print("\nCongratulations! You have SURVIVED The Purge.")
        print(f"Final Health: {player_health}%")
    else:
        print("\nYou did not survive...")
        print("GAME OVER.")


# --- Start the game ---
if __name__ == "__main__":
    game_loop()
