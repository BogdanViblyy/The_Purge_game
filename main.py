# main.py

import time
import os
import random

# ==============================================================================
# SPRINT 1: BASIC STRUCTURE AND INITIAL DATA
# ==============================================================================

# --- Game Configuration ---
PLAYER_INITIAL_HEALTH = 100
PLAYER_INITIAL_FOOD = 50
PLAYER_INITIAL_ENERGY = 100
SURVIVAL_GOAL_HOURS = 24

# --- Player State ---
player_health = PLAYER_INITIAL_HEALTH
player_food = PLAYER_INITIAL_FOOD
player_energy = PLAYER_INITIAL_ENERGY
hours_survived = 0

# ==============================================================================
# SPRINT 3: ENHANCING THE GAME (added earlier for better structure)
# ==============================================================================
# We add these new state variables as part of Sprint 3's enhancements.
shelter_level = 1
# Inventory: {item_name: quantity}
inventory = {
    "Medkit": 1,
    "Canned Food": 2
}
last_message = "" # To store messages from events or actions


# --- Helper Functions ---
def clear_console():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_status():
    """Displays the current status of the player and their shelter."""
    global last_message
    clear_console()
    print("=================================================")
    print(f"==          THE PURGE - HOUR: {hours_survived:02d}/{SURVIVAL_GOAL_HOURS}          ==")
    print("=================================================")
    print(f"  Health: {player_health:<5} Food: {player_food:<5} Energy: {player_energy:<5}")
    print(f"  Shelter Level: {shelter_level}")
    print("-------------------------------------------------")
    print("  Inventory:")
    if not inventory or all(v == 0 for v in inventory.values()):
        print("    - Empty")
    else:
        for item, count in inventory.items():
            if count > 0:
                print(f"    - {item}: {count}")
    print("=================================================")
    if last_message:
        print(f"\n>> {last_message}\n")
        last_message = "" # Clear message after displaying

# ==============================================================================
# SPRINT 2: ADDING THREATS AND CHOICES
# ==============================================================================
def handle_random_event():
    """Simulates a random event that can occur each hour."""
    global player_health, player_food, last_message, shelter_level

    # The better the shelter, the lower the chance of a bad event.
    # Sprint 3 Enhancement: Shelter level affects event probability.
    event_chance = random.randint(1, 100)
    
    # A high roll is needed to trigger a bad event. Better shelter increases the required roll.
    if event_chance > 60 + (shelter_level * 5):
        event_type = random.choice(["noise", "intruder", "wind"])
        
        if event_type == "noise":
            damage = random.randint(5, 10)
            player_health -= damage
            last_message = f"You hear a loud crash outside. The stress damages your health by {damage}!"
        
        elif event_type == "intruder":
            damage = random.randint(10, 20)
            player_health -= damage
            last_message = f"An intruder tried to break in! You fought them off, but lost {damage} health."
            
        elif event_type == "wind":
            food_lost = random.randint(5, 15)
            player_food -= food_lost
            last_message = f"A strong gust of wind blows open a window, spoiling {food_lost} food."
    # A low roll might trigger a good event
    elif event_chance < 10:
        last_message = "The night is surprisingly quiet. You feel a moment of peace."
    else:
        # No event happens
        pass


def get_player_action():
    """Gets and handles the player's choice for the hour."""
    global player_health, player_food, player_energy, shelter_level, inventory, last_message

    # ==========================================================================
    # SPRINT 3: ENHANCING CHOICES
    # ==========================================================================
    # The actions are more detailed and interact with the inventory and shelter.
    
    print("What will you do?")
    print("1. Rest (Consume 5 Food, a little Energy, to regain Health)")
    print("2. Scavenge for Supplies (Risky, consumes Energy)")
    print("3. Fortify Shelter (Consumes Energy, increases Shelter Level)")
    print("4. Use an Item from Inventory")

    choice = input("> ")

    if choice == '1':
        if player_food >= 5:
            player_food -= 5
            player_energy -= 5
            health_gained = random.randint(10, 15)
            player_health += health_gained
            last_message = f"You rested and ate some food. Gained {health_gained} health."
        else:
            last_message = "Not enough food to rest properly!"

    elif choice == '2':
        player_energy -= 20
        scavenge_chance = random.randint(1, 100)
        if scavenge_chance > 70:
            found_item = random.choice(["Canned Food", "Medkit"])
            inventory[found_item] = inventory.get(found_item, 0) + 1
            last_message = f"Success! You found a {found_item}."
        elif scavenge_chance > 40:
            food_found = random.randint(10, 20)
            player_food += food_found
            last_message = f"You found {food_found} food supplies."
        else:
            damage = random.randint(10, 15)
            player_health -= damage
            last_message = f"You were ambushed while scavenging! Lost {damage} health."

    elif choice == '3':
        if player_energy >= 30:
            player_energy -= 30
            shelter_level += 1
            last_message = f"You spent time fortifying your shelter. It is now Level {shelter_level}."
        else:
            last_message = "You are too exhausted to fortify the shelter."

    elif choice == '4':
        use_item()
    else:
        last_message = "Invalid choice. You hesitate and waste time."
        player_energy -= 5 # Penalty for indecisiveness

def use_item():
    """Handles the logic for using an item from the inventory."""
    global player_health, player_food, inventory, last_message

    print("Which item to use?")
    item_list = [item for item, count in inventory.items() if count > 0]
    if not item_list:
        last_message = "Your inventory is empty."
        return

    for i, item_name in enumerate(item_list):
        print(f"{i+1}. {item_name} ({inventory[item_name]})")

    try:
        choice_idx = int(input("> ")) - 1
        if 0 <= choice_idx < len(item_list):
            item_to_use = item_list[choice_idx]
            
            if item_to_use == "Medkit":
                player_health += 50
                inventory[item_to_use] -= 1
                last_message = "You used a Medkit and regained 50 health."
            elif item_to_use == "Canned Food":
                player_food += 40
                inventory[item_to_use] -= 1
                last_message = "You ate Canned Food and restored 40 food."
        else:
            last_message = "Invalid item choice."
    except ValueError:
        last_message = "Invalid input."

# --- Main Game Loop ---
def game_loop():
    global player_health, player_food, player_energy, hours_survived, last_message

    clear_console()
    print("--- THE PURGE HAS BEGUN ---")
    print(f"You must survive for {SURVIVAL_GOAL_HOURS} hours. Good luck.\n")
    input("Press Enter to begin...")

    while player_health > 0 and hours_survived < SURVIVAL_GOAL_HOURS:
        # 1. Display current status
        display_status()

        # 2. Player makes a choice (Feature from Sprint 2/3)
        get_player_action()
        
        # 3. Handle a random event (Feature from Sprint 2)
        handle_random_event()

        # 4. Update game state for the hour passing (Core from Sprint 1)
        # Passive consumption is removed; resource use is now tied to actions.
        # But we can add a small passive energy drain.
        player_energy -= 2 
        
        # 5. Check consequences of low resources
        if player_food <= 0:
            player_health -= 5
            player_food = 0
            # Prepend to last_message if it exists, otherwise set it
            starvation_msg = "You are starving! (-5 Health)"
            last_message = f"{starvation_msg} | {last_message}" if last_message else starvation_msg

        if player_energy <= 0:
            player_health -= 3
            player_energy = 0
            exhaustion_msg = "You are exhausted! (-3 Health)"
            last_message = f"{exhaustion_msg} | {last_message}" if last_message else exhaustion_msg

        # 6. Clamp values to be within bounds
        player_health = max(0, min(100, player_health))
        player_food = max(0, min(100, player_food))
        player_energy = max(0, min(100, player_energy))

        # 7. Advance time
        hours_survived += 1

        # 8. Pause for user to read the results
        display_status()
        input("\nPress Enter to proceed to the next hour...")


    # --- End of Game ---
    clear_console()
    print("=================================================")
    print("==           THE NIGHT IS OVER               ==")
    print("=================================================")
    if player_health > 0:
        print("\nCongratulations! You have SURVIVED The Purge.")
        print(f"Final Health: {player_health}%")
        print(f"Final Shelter Level: {shelter_level}")
    else:
        print("\nYou did not make it through the night...")
        print("GAME OVER.")


# --- Start the game ---
if __name__ == "__main__":
    game_loop()
