from db_setting import *
import random
from geopy import distance

# select 20 random airports for the game
def get_airports():
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


# get animals
def get_animals():
    db = get_db()
    db.execute("SELECT * FROM animals ORDER BY RAND() LIMIT 8")
    result = db.fetchall()
    return result

def get_item():
    db = get_db()
    db.execute("SELECT * FROM items")
    result = db.fetchall()
    return result


# get items
def check_item(game_id, current_airport):
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

# check if airport has animal
def check_animal(game_id, current_airport):
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


def prepare_items():
    # prepare items
    items = get_item()
    items_list = []
    for item in items:
        for i in range(item['quantity']):
            items_list.append(item['id'])
    return items_list


# create new game
def new_game(money, turns_time, start_airport, player, player_range, all_animals, g_ports, items_list):
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



# update animals location
    # not all 8 but random number from 1 to 8


# store saved animals
    # query to insert rescued animals into the 'rescued_animals' table


#set items found/opened




# get airport info
def get_airport_info(icao):
    db = get_db()
    db.execute("""
    SELECT iso_country, ident, name, latitude_deg, longitude_deg 
    FROM airport
    WHERE ident = %s
    """, (icao,))
    result = db.fetchone()
    return result





# calculate distance between two airports
def calculate_distance(current, target):
    start = get_airport_info(current)
    end = get_airport_info(target)
    return distance.distance((start['latitude_deg'], start['longitude_deg']),
                             (end['latitude_deg'], end['longitude_deg'])).km

# get airports in range
def airports_in_range(icao, a_ports, p_range):
    in_range = []
    for a_port in a_ports:
        dist = calculate_distance(icao, a_port['ident'])
        if dist <= p_range and not dist == 0:
            in_range.append(a_port)
    return in_range

# update location ###NEED add updating the time
def update_location(icao, p_range, u_money, time, g_id):
    db = get_db()
    db.execute( f'''UPDATE game SET location = %s, player_range = %s, money = %s, turn_time =%s  WHERE id = %s''', (icao, p_range, u_money, time, g_id),)



#DELEVERY FUNCTIONS


# choose the action function
def choose_action():
    options = ["1", "2", "3", "4", "5", "6"]
    while True:
        action = input("""
What do you do?:
(1) Check your balance;
(2) Buy fuel;
(3) Choose the airport to go
(4) Check rescued animals
(5) Check animals to rescue
(6) Exit game
> """).strip()
        if action not in options:
            prred("Choose a valid option. ")
            continue

        return int(action)

# use 'f_p' instead of 2
def buy_fuel(money, player_range):
    while True:
        fuel = input("How much fuel do you want to buy(1$ = 2km of range). Enter amount or press Enter ").upper()
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
        player_range += fuel * 2
        money -= fuel
        print(f"You have now {money:.0f}$ and {player_range:.0f}km of range")
        return money, player_range

def get_rescued(game_id):
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

def return_chance():
    a = random.randint(0,10)
    if a == 9 or a == 10 or a == 8:
        return False
    return True


def insert_rescued_animals(animal, game_id):
    db = get_db()
    db.execute(
        "INSERT INTO rescued_animals(game_id, animal_id) VALUES(%s, %s)",
        (game_id, animal['animals_id']), )
    db.execute(
        "UPDATE located_animals SET rescued = 1 WHERE game_id = %s and animal_id = %s",
        (game_id, animal['animals_id'], )
    )

def count_animals(g_id):
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

def pause():
    input("\nPress Enter to continue > ")


def open_item(game_id, item):
    db = get_db()
    db.execute(
        "UPDATE located_items SET opened = 1 WHERE game_id = %s and item_id = %s",
        (game_id, item['item_id'], )
    )



"""Update items, animals locations in 'located_items' and 'located_animals' """



"""Returns the name of the current airport"""
def position_airport(game_id):
    db = get_db()
    db.execute("SELECT a.name FROM airport a JOIN game ON a.ident = game.location WHERE game.id = %s", (game_id,))
    result = db.fetchone()
    return result

def sorted_airports(airports, current_airport):
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




def prred(s): print("\033[91m {}\033[00m".format(s))
def prgreen(s): print("\033[92m {}\033[00m".format(s))
def pryellow(s): print("\033[93m {}\033[00m".format(s))
def prlightpurple(s): print("\033[94m {}\033[00m".format(s))
def prpurple(s): print("\033[95m {}\033[00m".format(s))
def prblack(s): print("\033[90m {}\033[00m".format(s))