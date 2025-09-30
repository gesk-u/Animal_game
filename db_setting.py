import mysql.connector
import threading

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
            database="animals_game",
            autocommit=True
        )
        g['conn'] = conn
        g['db'] = conn.cursor(dictionary=True)
    return g['db']