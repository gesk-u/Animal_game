from func import *
import story

def main():
    # === PLAYER SETUP ===
    # Ask for player name and whether to show the story
    player = input("type player name: ")
    storyDialog = input("Do you want to read the background story? (Y/N): ").upper()

    # Display story if chosen
    if storyDialog == 'Y':
        # print wrapped string line by line
        for line in story.getStory(player):
            print(line)
    # GAME SETTINGS
    pause()


    # === INITIAL GAME SETTINGS ===
    game_over = False       # Main game loop flag
    money = 1000            # Starting money
    player_range = 5000     # Starting range in km
    days = 5                # Total number of turns per cycle
    one_turn = 1            # How much a single action consumes
    turns_time = days       # Remaining turns counter
    f_p = 2                 # Fuel price (1$ = 2km of range)
    resc_num = 0

    # === LOAD GAME DATA FROM DATABASE ===
    all_airports = get_airports()       # List of 20 random airports
    g_ports = all_airports[1:].copy()   # Copy all except the first (used for distributing animals/items)
    all_animals = get_animals()         # Random list of animals
    items_list = prepare_items()        # Prepare item list (IDs repeated by quantity)
    history = []                        # To track visited airports

    # === STARTING LOCATION ===
    start_airport = all_airports[0]["ident"]
    start_p_name = all_airports[0]["name"]
    current_airport = start_airport

    # Intro text
    print(f"\nThe last traces of Matti lead to {color_text(start_p_name, 'blue')}")
    print(f"\nYou have {color_text(f'{money:.0f}$', 'yellow')} and {color_text(f'{player_range:.0f}km', 'yellow')} of range for the start")
    print("\nThere are no animals here! Keep going!")
    pause()

    # Create new game in the database
    game_id = new_game(money, turns_time, start_airport, player, player_range, all_animals, g_ports, items_list)
    first_loop = True   # Used to suppress repeated location messages at start



    # === MAIN GAME LOOP ===
    while not game_over:
        # --- Update game state ---
        airport = position_airport(game_id)             # Current airport info
        animal = check_animal(game_id, current_airport) # Check for unrescued animals
        item = check_item(game_id, current_airport)     # Check for unopened items

        # Display current airport (skip first loop to avoid repeating)
        if not first_loop:
            print(f"You are at {airport['name']}")

        # --- Handle animal discovery ---
        if animal:
            print(f"Amazing! You found animals this is {animal['description']}\n")
            print(f"Press Enter to rescue {animal['name']}")
            insert_rescued_animals(animal, game_id)
            pause()

        # --- Handle item discovery ---
        if item:
            print(f"It looks like somebody left {item['name']} bag ")
            item_question = input(f"Do you want to spend your day and try to find the owner and get a money reward? (Y/N): ").upper()

            if item_question == "Y":
                open_item(game_id, item)
                turns_time -= one_turn
                found = return_chance()

                if found:
                    print(f"Oh! you found the owner of the {item['name']} bag and receive a reward of {item['price']}$!")
                    money = money + int(item['price'])
                    #pause
                    pause()
                else:
                    print("You spent all day looking for the owner, but without success.")
                    pause()
            else:
                pause()
        # --- Main menu actions ---
        action = choose_action()

        # (1) Check balance
        if action == 1:
            print(
                f"\nYou have {color_text(f'{money:.0f}$', 'yellow')} and {color_text(f'{player_range:.0f}km', 'yellow')} of range")
            pause()

        # (2) Buy fuel
        elif action == 2:
            money, player_range = buy_fuel(money, player_range, f_p)
            pause()

        # (3) Choose next airport
        elif action == 3:
            # Get airports within reachable range
            airports = airports_in_range(current_airport, all_airports, player_range)
            print(f"\nThere are {color_text(str(len(airports)), 'yellow')} airports in range:")

            # If none reachable, force player to buy fuel
            if len(airports) == 0:
                while money > 0 and len(airports) == 0:
                    print(f"Looks like you do not have a fuel. Lets buy some and see if the are any available airports to reach\nMoney: {money:.0f}$")
                    money, player_range = buy_fuel(money, player_range, f_p)
                    airports = airports_in_range(current_airport, all_airports, player_range)
            
                if len(airports) == 0:
                    prred("No airports in range and no money left. Game over!")
                    game_over = True
            else:
                # Display airports sorted by distance
                print("Airports: \n")
                sort_airports = sorted_airports(airports, current_airport)
                ap_icao = []
                for ap in sort_airports:
                    ap_icao.append(ap['icao'])
                for ap in sort_airports:
                    print(f"{ap['icao']} - {ap['name']} ({color_text(str(ap['distance_km']), 'yellow')}km)")

                print("\nVisited: ", end="")
                for i in range(len(history)):
                    end_char = ", " if i < len(history) - 1 else ""
                    print(color_text(history[i], 'yellow'), end=end_char)
                print("\n")
                while True:
                    # Choose destination
                    dest = input("Enter destination icao or press Enter to go to menu: ").upper()
                    history.append(dest)


                    if dest == "":
                        pass
                        break

                    # If destination entered, travel there
                    elif dest in ap_icao:
                        selected_distance = calculate_distance(current_airport, dest)
                        player_range -= selected_distance
                        turns_time -= one_turn
                        update_location(dest, player_range, money, turns_time, game_id)
                        current_airport = dest
                        break

                    else:
                        prred("\nSelect airport icao from the list ot press Enter\n")


                # Check fuel after move
                if player_range < 0:
                    while money > 0:
                        print(f"Looks like you do not have a fuel. Lets buy some \nMoney: {money:.0f}$")
                        money, player_range = buy_fuel(money, player_range, f_p)
            pause()

        # (4) Check rescued animals
        elif action == 4:
            print("Rescued animals: \n")
            rescued_animals = get_rescued(game_id)
            for resc_num, animal in enumerate(rescued_animals, start=1):
                print(f"{resc_num}. {animal['name']}")
            pause()

        # (5) Check animals to rescue
        elif action == 5:
            print(f"\nAnimals to rescue: {color_text(count_animals(game_id), 'yellow')}")
            pause()

        else:
            game_over = True


        # Win condition: all animals rescued
        if resc_num == len(all_animals):
            print("You rescued all animals. Evil Matti will never steal them again")
            game_over = True

        # Time expired: reset locations and turns
        if turns_time == 0:
            del history
            update_all(game_id, all_animals, g_ports)
            turns_time = days

        # Disable first-loop behavior after first iteration
        if first_loop:
            first_loop = False



if __name__ == "__main__":
    main()



