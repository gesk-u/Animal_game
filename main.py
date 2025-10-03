from func import *
import story

def main():
    # ask to show the story
    # add lowercase and strip()
    storyDialog = input("Do you want to read the background story? (Y/N): ")
    if storyDialog == 'Y':
        # print wrapped string line by line
        for line in story.getStory():
            print(line)
    # GAME SETTINGS
    print("When you are ready to start, ")
    player = input("type player name: ")

    # boolean for game over and print
    game_over = False

    # start money = 1000
    money = 1000
    # start range in km = 2000
    player_range = 5000

    # time = 15 turns
    days = 15
    one_turn = 1
    turns_time = days


    # fuel price
    f_p = 2

    # all airports
    all_airports = get_airports()
    g_ports = all_airports[1:].copy()
    all_animals = get_animals()
    items_list = prepare_items()

    # start airport ident
    start_airport = all_airports[0]["ident"]
    start_p_name = all_airports[0]["name"]

    # current airport
    current_airport = start_airport

    # Matti is bad guy change it
    # add spaces thoughout the game
    print(f"Matti has led you to {start_p_name}")
    print(f"He gave you {money:.0f}$ and {player_range:.0f}km of range for the start")
    print("There are no animals here! Keep going!")
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

        if animal:
            print(f"Amazing! You found animals this is {animal['description']}\n")
            print(f"Press Enter to rescue {animal['name']}")
            insert_rescued_animals(animal, game_id)
            pause()


        # ask if want to look for item
        if item:
            print(f"It looks like somebody left {item['name']} bag ")
            item_question = input(f"Do you want to spend your day and try to find the owner and get a money reward? (Y/N): ")
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



        if not first_loop:
            print(f"You are at {airport['name']}")


        action = choose_action()

        if action == 1:
            print(f"Money: {money:.0f}$;\nRange: {player_range:.0f}km;\nTime: {turns_time} days left.")
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
                    print("No airports in range and no money left. Game over!")
                    game_over = True
            else:
                print("Airports: ")
                sort_airports = sorted_airports(airports, current_airport)
                for ap in sort_airports:
                    print(f"{ap['icao']} - {ap['name']} ({ap['distance_km']} km)")

                # ask for destination
                dest = input("Enter destination icao: ")
                selected_distance = calculate_distance(current_airport, dest)
                player_range -= selected_distance
                turns_time = turns_time - one_turn
                update_location(dest, player_range, money, turns_time, game_id)
                current_airport = dest

                if player_range < 0:
                    while money > 0:
                        print("Looks like you do not have a fuel. Lets buy some")
                        money, player_range = buy_fuel(money, player_range)
            pause()


        elif action == 4:
            print("Rescued animals: ")
            rescued_animals = get_rescued(game_id)
            for i, animal in enumerate(rescued_animals, start=1):
                print(f"{i}. {animal['name']}")
            pause()

        elif action == 5:
            print(f"Animals to rescue: {count_animals(game_id)}")
            pause()

        else:
            game_over = True
        if first_loop:
            first_loop = False

        if turns_time == 0:
            print(
                "Oh no! Evil Matti moved animals to the different airports!",
                "\n Hurry up! and find remaining animals!"
                  )
            relocate_all(turns_time, all_animals, game_id, g_ports)
            turns_time = days
















if __name__ == "__main__":
    main()



