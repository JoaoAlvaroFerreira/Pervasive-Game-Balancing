import sqlite3
from View.gui import screen
from Model.player import Player
import Controller.PlayerSimulation
from sqlite3 import Error

def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def create_tables(conn):
  
    try:
        cursor = conn.cursor()
        sql_file = open(".\Databases\gamedb.sql")
        sql_as_string = sql_file.read()
        cursor.executescript(sql_as_string)
       
    except Error as e:
        print(e)

def insert_game(conn):
    sql = ''' INSERT INTO Game(name,locationbased,timebased,socialexpansion)
              VALUES("Teste",true,true,true) '''
    cur = conn.cursor()
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid

def print_all_players(conn):
    cur = conn.execute("SELECT id, name from Player")
    for row in cur:
        print("ID ",row[0])
        print("Name: ",row[1])
    
    print ("The End")

    

    



if __name__ == '__main__':
    p = Player("Joao")
    print(p.name)
    connection = create_connection(".\Databases\games.db")
    create_tables(connection)
    insert_game(connection)
    p.insert_into_db(connection)
    print_all_players(connection)
    screen()
  
    #generate_players
    #add to db

    #normal use cycle