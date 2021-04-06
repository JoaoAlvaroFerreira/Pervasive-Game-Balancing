import sqlite3
from Model.player import Player
from Controller.GameManagement import *
from Controller.Simulation import *
from Controller.Analytics import *
from View.plots import *
import requests
import names
from sqlite3 import Error
import sys


DB_PATH = "D:\\School\\5oAno\\TESE\\Repo\\Pervasive-Game-Balancing\\Databases\\games.db"

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
        sql_file = open("D:\\School\\5oAno\\TESE\\Repo\\Pervasive-Game-Balancing\\Databases\\gamedb.sql")
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

    #connection = create_connection(".\Databases\games.db")
    #create_tables(connection)
    #insert_game(connection)
    #print_all_players(connection)
    #screen()

    if len(sys.argv) < 2:
        print("Use python ./main <create|sim|plot|analyse>")
        exit()

    if sys.argv[1] == "create":
        game = GameManagement()
        connection = create_connection(DB_PATH)
        create_tables(connection)
        insert_game(connection)
        game.create(connection)

    elif sys.argv[1] == "sim":
        game = GameManagement()
        connection = create_connection(DB_PATH)
        game.load(connection)
        sim = Simulation(game)
        sim.sim()
    
    elif sys.argv[1] == "plot":
        game = GameManagement()
        connection = create_connection(DB_PATH)
        game.load(connection)
        plot_players(game.players)    
        #plotplot()   

    elif sys.argv[1] == "analyse":
        game = GameManagement()
        connection = create_connection(DB_PATH)
        game.load(connection)
        an = Analytics(game)
        an.analyse_players() 
    
    else: print("Use python ./main <create|sim|plot>")


    
    
   
  
    #add to db

    #normal use cycle