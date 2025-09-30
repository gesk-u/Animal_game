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
    db.execute("SELECT name FROM animals ORDER BY RAND() LIMIT 8")
    result = db.fetchall()
    return result

# get items
def check_item(game_id, current_airport):
    db = get_db()
    db.execute("""
    SELECT located.item_id, items.id as item_id, items.name, items.price
    FROM located
    JOIN items ON items.id = located.item_id
    WHERE game_id = %s
    AND location = %s;
    """, (game_id, current_airport), )

    result = db.fetchall()
    return result


# create new game

def new_game(money, turns_time, start_airport, player, player_range, all_airports, all_animals):
    db = get_db()

    # insert gamer data to game table: id, money, turns_time, start_airport, name, range
    db.execute("INSERT INTO game(screen_name, money, player_range, location, turn_time)  VALUES (%s, %s, %s, %s, %s)", (player, money, player_range, start_airport, turns_time))
    
    # add items
    # use get_goal() function to get variable 'goals'
    items = get_items()

        # make empty list of items
    items_list = []

    #iterate 'goals' from 0 to its quantity to append to the empty list
    for item in items:
        for i in range(0, items['quantity'], 1):
            items_list.append(item['id'])
        
    # exclude starting airport



    # insert game_id, animals, items, location (for each animal and item),  into located table





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


# check if airport has animal
def check_animal(game_id, current_airport):
    db = get_db()
    db.execute("""
    SELECT located.animal_id, animals.id as animals_id, animals.name
    FROM located
    JOIN animals ON animals.id = located.animal_id
    WHERE game_id = %s 
    AND location = %s
    """, (game_id, current_airport),)
    result = db.fetchone()
    print()
    print(result)
    if result is None:
        return False
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
#def update_location(icao, p_range, u_money, g_id):
    db = get_db()
    db.execute( f'''UPDATE game SET location = %s, player_range = %s, money = %s WHERE id = %s''', (icao, p_range, u_money, g_id),)



#DELEVERY FUNCTIONS
