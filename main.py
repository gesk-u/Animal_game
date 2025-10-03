from func import *
import story

def main():
    # ask to show the story
    # add lowercase and strip()
    storyDialog = input("Do you want to read the background story? (Y/N): ").upper()
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
    player_range = 2000

    # time = 15 turns
    one_turn = 1
    turns_time = 15


    # fuel price
    f_p = 2

    # all airports
    all_airports = get_airports()
    all_animals = get_animals()

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
    game_id = new_game(money, turns_time, start_airport, player, player_range, all_airports, all_animals)
    # GAME LOOP
    while not game_over:
        # get current airport info
        airport = get_airport_info(current_airport)


        item = check_item(game_id, current_airport)
        animal = check_animal(game_id, current_airport)

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

        if animal:
            print(f"Amazing! You found animals this is {animal['description']} {animal['name']} waiting at this airport.")
            insert_rescued_animals(animal, game_id)
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
                    prgreen("Looks like you do not have a fuel. Lets buy some and see if the are any available airports to reach")
                    money, player_range = buy_fuel(money, player_range)
                    airports = airports_in_range(current_airport, all_airports, player_range)
                if len(airports) == 0:
                    prred("No airports in range and no money left. Game over!")
            else:
                print("Airports: ")
                for airport in airports:
                    ap_distance = calculate_distance(current_airport, airport["ident"])
                    print(f"{airport['name']}, icao: {airport['ident']}, distance: {ap_distance:.0f}km")


                # ask for destination
                dest = input("Enter destination icao or press Enter to go to menu: ").upper()
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















if __name__ == "__main__":
    main()



