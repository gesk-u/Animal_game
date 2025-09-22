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
    # start airport ident
    start_airport = all_airports[0]["ident"]
    # current airport
    current_airport = start_airport

    all_animals = get_animals()








if __name__ == "__main__":
    main()



