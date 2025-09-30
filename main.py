from func import *
import story

def main():
    # ask to show the story
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
    win = False

    # start money = 1000
    money = 1000
    # start range in km = 2000
    player_range = 2000

    # time = 15 turns
    turns_time = 15

    # fuel price
    f_p = 2

    # all airports
    all_airports = get_airports()
    """Test"""
    print(get_airports())
    # start airport ident
    start_airport = all_airports[0]["ident"]
    """Test"""
    print(f"Start airport: {start_airport}")
    # current airport
    current_airport = start_airport

    all_animals = get_animals()
    """Test"""
    print(get_animals())

    # game_id = new_game(money, turns_time, start_airport, player, player_range, all_airports, all_animals)
    # GAME LOOP
    while not game_over:
        # get current airport info
        airport = get_airport_info(current_airport)
        # Current location information
        print(f"Matti has led you to {airport['name']}")
        print(f"He gave you {money}$ and {player_range} of fuel for the start")
        print("There are no animals here! Keep going!")
        #pause
        input("Press Enter to start!")

        item = check_item(game_id, current_airport)
        animal = check_animal(game_id, current_airport)

        if item:
            print(f"Oh! you found {item["name"]} box and you will receive {item["money"]}$!")
            money = money + int(item["money"])
            #pause
            input("Press Enter to continue")














if __name__ == "__main__":
    main()



