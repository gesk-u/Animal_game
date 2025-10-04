from db_setting import *
import random
from geopy import distance


def choose_action():
    """ Display the main action menu and prompt the player to choose an option. """
    options = ["1", "2", "3", "4", "5", "6"]
    while True:
        action = input("""
What do you do?:
(1) Check your balance;
(2) Buy fuel;
(3) Choose the airport to go
(4) Check rescued animals
(5) Check animals to rescue
(6) Exit game\n
> """).strip()
        if action not in options:
            prred("Choose a valid option. ")
            continue

        return int(action)


def prepare_items():
    """ Prepare a list of item IDs based on their quantities. """
    # prepare items
    items = get_item()
    items_list = []
    for item in items:
        for i in range(item['quantity']):
            items_list.append(item['id'])
    return items_list


def calculate_distance(current, target):
    """ Calculate the distance (in kilometers) between two airports. """
    start = get_airport_info(current)
    end = get_airport_info(target)
    return distance.distance((start['latitude_deg'], start['longitude_deg']),
                             (end['latitude_deg'], end['longitude_deg'])).km


def airports_in_range(icao, a_ports, p_range):
    """ Find all airports that are within a range from the player's current location. """
    in_range = []
    for a_port in a_ports:
        dist = calculate_distance(icao, a_port['ident'])
        if dist <= p_range and not dist == 0:
            in_range.append(a_port)
    return in_range


def sorted_airports(airports, current_airport):
    """ Sort a list of airports by their distance from the current location. """
    airport_distances = []
    for airport in airports:
        ap_distance = calculate_distance(current_airport, airport["ident"])
        airport_distances.append({
            "icao": airport["ident"],
            "name": airport["name"],
            "distance_km": round(ap_distance)
        })
        airport_distances.sort(key=lambda x: x["distance_km"])
    return airport_distances


def buy_fuel(money, player_range, f_p):
    """ Handle the process of buying fuel """
    while True:
        fuel = input(f"\nMoney: {money:.0f}$\nHow much fuel do you want to buy(1$ = 2km of range). Enter amount or press Enter ").upper()
        if fuel.strip() == "":
            print("No fuel purchased")
            return money, player_range
        try:
            fuel = float(fuel)
        except ValueError:
            print("Please enter a number.")
            continue
        if fuel > money:
            print("You do not have enough money.")
            continue
        if fuel <= 0:
            print("You must buy a positive amount of fuel")
            continue
        player_range += fuel * f_p
        money -= fuel
        print(f"You have now {money:.0f}$ and {player_range:.0f}km of range")
        return money, player_range


def return_chance():
    """ Random 70% success and 30% chance of failure """
    a = random.randint(0,10)
    if a == 9 or a == 10 or a == 8:
        return False
    return True



# ======================================
# DATABASE FUNCTIONS
# ======================================


def get_airports():
    """ Retrieve a random selection of large airports located in Europe. """
    db = get_db()
    db.execute("""
        SELECT iso_country, ident, name, type, latitude_deg, longitude_deg
        FROM airport
        WHERE continent = 'EU'
        AND type = 'large_airport'
        ORDER BY RAND()
        LIMIT 20
    """)
    result = db.fetchall()
    return result


def get_animals():
    """ Retrieve a random selection of animals """
    db = get_db()
    db.execute("SELECT * FROM animals ORDER BY RAND() LIMIT 3")
    result = db.fetchall()
    return result


def get_item():
    """ Retrieve all items from the database """
    db = get_db()
    db.execute("SELECT * FROM items")
    result = db.fetchall()
    return result


def new_game(money, turns_time, start_airport, player, player_range, all_animals, g_ports, items_list):
    """ Create a new game session and initialize all related data. """
    db = get_db()
    # insert gamer data to game table: id, money, turns_time, start_airport, name, range
    db.execute(
        "INSERT INTO game(screen_name, money, player_range, location, turn_time)  VALUES (%s, %s, %s, %s, %s)",
        (player, money, player_range, start_airport, turns_time)
    )
    g_id = db.lastrowid

    # exclude starting airport
    random.shuffle(g_ports)
    # insert game_id, animals, items, location (for each animal and item),  into located table
    for i, item_id in enumerate(items_list):
        db.execute("INSERT INTO located_items(item_id, game_id, location) VALUES(%s, %s, %s)",
                   (item_id, g_id, g_ports[i]['ident']))

    random.shuffle(g_ports)
    for i, animal in enumerate(all_animals):
        db.execute(
            "INSERT INTO located_animals(animal_id, game_id, location) VALUES(%s, %s, %s)",
            (animal['id'], g_id, g_ports[i]['ident'])
        )
    return g_id


def check_item(game_id, current_airport):
    """ Check if there is an unopened item located at the current airport for this game. """
    db = get_db()
    db.execute("""
    SELECT items.id as item_id, items.name, items.price, located_items.opened
    FROM located_items
    JOIN items ON items.id = located_items.item_id
    WHERE game_id = %s
    AND location = %s;
    """, (game_id, current_airport), )

    result = db.fetchone()
    if not result:
        return None
    if result['opened'] == 0:
        return result
    return None


def check_animal(game_id, current_airport):
    """ Check if there is an unrescued animal located at the current airport. """
    db = get_db()
    db.execute("""
    SELECT animals.id as animals_id, animals.name, animals.description, l.rescued
    FROM located_animals l
    JOIN animals ON animals.id = l.animal_id
    WHERE game_id = %s 
    AND location = %s
    """, (game_id, current_airport), )
    result = db.fetchone()
    if not result:
        return None
    if result['rescued'] == 0:
        return result
    return None


def update_location(icao, p_range, u_money, time, g_id):
    """  Update the player's location, range, money, and time in the current game. """
    db = get_db()
    db.execute( f'''UPDATE game SET location = %s, player_range = %s, money = %s, turn_time =%s  WHERE id = %s''', (icao, p_range, u_money, time, g_id),)


def update_all(game_id, all_animals, g_ports):
    """ Shuffle and update the locations of all animals and items for a given game. """
    db = get_db()
    random.shuffle(g_ports)
    for i, animal in enumerate(all_animals):
        db.execute("""
        UPDATE located_animals 
        SET location = %s
        WHERE animal_id = %s
        AND game_id = %s;
        """, (g_ports[i]['ident'], animal['id'], game_id, ) )

    db.execute("DELETE FROM located_items WHERE game_id = %s;", (game_id, ))
    random.shuffle(g_ports)
    item_list = prepare_items()
    for i, item_id in enumerate(item_list):
        db.execute("INSERT INTO located_items(item_id, game_id, location) VALUES(%s, %s, %s)",
                   (item_id, game_id, g_ports[i]['ident']))


def get_airport_info(icao):
    """ Retrieve information about a specific airport by its ICAO code. """
    db = get_db()
    db.execute("""
    SELECT iso_country, ident, name, latitude_deg, longitude_deg 
    FROM airport
    WHERE ident = %s
    """, (icao,))
    result = db.fetchone()
    return result


def position_airport(game_id):
    """ Retrieve the name of the current airport """
    db = get_db()
    db.execute("SELECT a.name FROM airport a JOIN game ON a.ident = game.location WHERE game.id = %s", (game_id,))
    result = db.fetchone()
    return result


def get_rescued(game_id):
    """ Retrieve all animals that have been rescued in the current game. """
    db = get_db()
    db.execute("""
    SELECT a.name
    FROM animals a
    JOIN rescued_animals r
        ON a.id = r.animal_id
    WHERE r.game_id = %s
        """, (game_id,) )
    result = db.fetchall()
    if not result:
        prred("You did not rescue any animals yet! Hurry up!")
    return result


def insert_rescued_animals(animal, game_id):
    """  Mark an animal as rescued and add it to the rescued_animals table. """
    db = get_db()
    db.execute(
        "INSERT INTO rescued_animals(game_id, animal_id) VALUES(%s, %s)",
        (game_id, animal['animals_id']), )
    db.execute(
        "UPDATE located_animals SET rescued = 1 WHERE game_id = %s and animal_id = %s",
        (game_id, animal['animals_id'], )
    )


def count_animals(g_id):
    """ Count the number of animals remaining to be rescued in the current game. """
    db = get_db()
    db.execute("""
        SELECT COUNT(l.animal_id) AS remaining
        FROM located_animals l
        JOIN animals ON animals.id = l.animal_id
        WHERE l.rescued = 0 and l.game_id = %s
        """, (g_id,)
    )
    result = db.fetchone()
    return result['remaining'] if result else 0


def open_item(game_id, item):
    """  Mark an item as opened in the database for the current game. """
    db = get_db()
    db.execute(
        "UPDATE located_items SET opened = 1 WHERE game_id = %s and item_id = %s",
        (game_id, item['item_id'], )
    )


# ======================================
# COLOR FUNCTIONS
# ======================================

def prred(s): print("\033[91m {}\033[00m".format(s))
def prgreen(s): print("\033[32m {}\033[00m".format(s))
def pryellow(s): print("\033[93m {}\033[00m".format(s))
def prlightpurple(s): print("\033[94m {}\033[00m".format(s))
def prpurple(s): print("\033[95m {}\033[00m".format(s))
def prblack(s): print("\033[90m {}\033[00m".format(s))


def color_text(text, color):
    colors = {
        "red": "\033[91m",
        "green": "\033[32m",
        "yellow": "\033[33m",
        "blue": "\033[94m",
        "purple": "\033[95m",
        "black": "\033[90m",
        "reset": "\033[0m"
    }
    return f"{colors.get(color, colors['reset'])}{text}{colors['reset']}"


def pause():
    """ Pause the game until the player presses Enter. """
    input(color_text("\nPress Enter to continue\n\n> ", "green"))
