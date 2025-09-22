import mysql.connector
import threading
import random
from geopy import distance

#Flask's g
_storage = threading.local() #"_"internal use # class container

def get_g():
    if not hasattr(_storage, "storage"):
        _storage.storage = {}
    return _storage.storage

def get_db():
    g = get_g()
    if 'db' not in g:
        conn = mysql.connector.connect(
            user="root",
            password="password",
            host="127.0.0.1",
            port=3306,
            database="project",
            autocommit=True
        )
        g['conn'] = conn
        g['db'] = conn.cursor(dictionary=True)
    return g['db']

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
    db.execute("SELECT name FROM anomals ORDER BY RAND() LIMIT 8")
    result = db.fetchall()
    return result

# get items


# create new game
    # exclude starting airport

    # add animals, items

    # insert animals items into located table



# update animals location
    # not all 8 but random number from 1 to 8



#set items found opened




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
def check_goal():
    db = get_db()
    db.execute("""""", (),)
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