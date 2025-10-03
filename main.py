from func import *
import story

def main():
    # ask to show the story
    # add lowercase and strip()
    player = input("type player name: ")
    storyDialog = input("Do you want to read the background story? (Y/N): ").upper()
    if storyDialog == 'Y':
        # print wrapped string line by line
        for line in story.getStory(player):
            print(line)
    # GAME SETTINGS
    print("When you are ready to start, ")


    # boolean for game over and print
    game_over = False

    # start money = 1000
    money = 1000
    # start range in km = 2000
    player_range = 5000

    # time = 15 turns
    days = 2
    one_turn = 1
    turns_time = days


    # fuel price
    f_p = 2

    # all airports
    all_airports = get_airports()
    g_ports = all_airports[1:].copy()
    all_animals = get_animals()
    items_list = prepare_items()
    history = []


    # start airport ident
    start_airport = all_airports[0]["ident"]
    start_p_name = all_airports[0]["name"]

    # current airport
    current_airport = start_airport

    # Matti is bad guy change it
    # add spaces thoughout the game

    prlightpurple(f"Matti has led you to {start_p_name}")
    pryellow(f"He gave you {money:.0f}$ and {player_range:.0f}km of range for the start")
    prgreen("There are no animals here! Keep going!")
    # pause
    pause()
    game_id = new_game(money, turns_time, start_airport, player, player_range, all_animals, g_ports, items_list)
    first_loop = True



    # GAME LOOP
    while not game_over:
        # get current airport info
        airport = position_airport(game_id)
        animal = check_animal(game_id, current_airport)
        item = check_item(game_id, current_airport)
        if not first_loop:
            print(f"You are at {airport['name']}")
        if animal:
            print(f"Amazing! You found animals this is {animal['description']}\n")
            print(f"Press Enter to rescue {animal['name']}")
            insert_rescued_animals(animal, game_id)
            pause()


        # ask if want to look for item
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






        action = choose_action()

        if action == 1:
            prpurple(f"You have {money:.0f}$ and {player_range:.0f}km of range")
            # pause
            pause()

        elif action == 2:
            money, player_range = buy_fuel(money, player_range)
            pause()

        elif action == 3:
            # show airports range
            airports = airports_in_range(current_airport, all_airports, player_range)
            print(f"There are {len(airports)} airports in range: ")

            if len(airports) == 0:
                while money > 0 and len(airports) == 0:
                    print(f"Looks like you do not have a fuel. Lets buy some and see if the are any available airports to reach\nMoney: {money:.0f}$")
                    money, player_range = buy_fuel(money, player_range)
                    airports = airports_in_range(current_airport, all_airports, player_range)
            
                if len(airports) == 0:
                    prred("No airports in range and no money left. Game over!")
                    game_over = True
            else:
                print("Airports: ")
                sort_airports = sorted_airports(airports, current_airport)
                for ap in sort_airports:
                    print(f"{ap['icao']} - {ap['name']} ({ap['distance_km']} km)")

                # ask for destination
                dest = input("Enter destination icao or press Enter to go to menu: ").upper()
                history.append(dest)
                print("Visited: ", end="")
                for i in range(len(history)):
                    print(f"{history[i]}" + ", ", end="")
                if dest == "":
                    pass
                else:
                  selected_distance = calculate_distance(current_airport, dest)
                  player_range -= selected_distance
                  turns_time -= one_turn
                  update_location(dest, player_range, money, turns_time, game_id)
                  current_airport = dest

                if player_range < 0:
                    while money > 0:
                        print("Looks like you do not have a fuel. Lets buy some")
                        money, player_range = buy_fuel(money, player_range)
            pause()


        elif action == 4:
            prlightpurple("Rescued animals: ")
            rescued_animals = get_rescued(game_id)
            for i, animal in enumerate(rescued_animals, start=1):
                pryellow(f"{i}. {animal['name']}")
            pause()

        elif action == 5:
            prblack(f"Animals to rescue: {count_animals(game_id)}")
            pause()

        else:
            game_over = True
        if first_loop:
            first_loop = False


        if turns_time == 0:
            update_all(game_id, all_animals, g_ports)
            turns_time = days

















if __name__ == "__main__":
    main()



