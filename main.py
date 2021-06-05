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
from Controller.ML import *


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
    
def clear_sim(conn):
    sql = ''' DELETE FROM PlayMoment;'''
    cur = conn.cursor()
    cur.execute(sql)
    sql= '''DELETE FROM ChallengeInstance;'''
    cur.execute(sql)
    conn.commit()
    return cur.lastrowid
    

def create():
    game = GameManagement()
    connection = create_connection(DB_PATH)
    create_tables(connection)
    insert_game(connection)
    game.create(connection)
    print("Done creating!")

def sim():
    game = GameManagement()
    connection = create_connection(DB_PATH)
    game.load(connection)
    clear_sim(connection)
    sim = Simulation(game)
    sim.sim()
    print("Done Simulating!")

def analyse():
    game = GameManagement()
    connection = create_connection(DB_PATH)
    game.load(connection)
    
    an = Analytics(game)
    return an.analyse_players() 

def ML(variable, value, max):
    game = GameManagement()
    connection = create_connection(DB_PATH)
    game.load(connection)
    an = Analytics(game)
    an.calc_average_KPIs()
    dataset = an.data_preprocessing()
    filtered = filter_data(dataset, variable, value, max)
    demos = random_forest(filtered, max)
    return an.demo_analysis(demos)

def full_ML():
    game = GameManagement()
    connection = create_connection(DB_PATH)
    game.load(connection)
    an = Analytics(game)
    an.calc_average_KPIs()
    dataset = an.data_preprocessing()
    early_triggers = an.early_triggers(dataset)
    #Challenges Done", "Lifetime Value", "Sessions
    filtered1 = filter_data(dataset, "Lifetime Value", 50, "Max")
    filtered2 = filter_data(dataset, "Challenges Done", 30, "Max")
    filtered3 = filter_data(dataset, "Sessions", 130, "Max")

    filtered4 = filter_data(dataset, "Lifetime Value", 2, "Min")
    filtered5 = filter_data(dataset, "Challenges Done", 2, "Min")
    filtered6 = filter_data(dataset, "Sessions", 10, "Min")
    combined_data_max = pd.concat([filtered1, filtered2, filtered3])
    combined_data_min = pd.concat([filtered4, filtered5,filtered6])
    demos_max = random_forest(combined_data_max, "")
    demos_min = random_forest(combined_data_min, "")
    conclusion_max = an.demo_analysis(demos_max)
    conclusion_min = an.demo_analysis(demos_min)
    
    return "EARLY ANALYSIS SHOWS...:\n"+early_triggers + "\n POSITIVE RESULTS: \n"+ conclusion_max + "\n NEGATIVE RESULTS:\n" + conclusion_min


def plot():
    game = GameManagement()
    connection = create_connection(DB_PATH)
    game.load(connection)
    return game

def plotmap():
    game = GameManagement()
    connection = create_connection(DB_PATH)
    game.load(connection)
    combined_plot(game.challenge_instances,game.gameplay_moments)    

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
       create()

    elif sys.argv[1] == "sim":
        sim()
    
    elif sys.argv[1] == "plot":
        game = GameManagement()
        connection = create_connection(DB_PATH)
        game.load(connection)
        heatmap_moments(game.moments)    
        #plotplot()   

    elif sys.argv[1] == "analyse":
        analyse()
    
    elif sys.argv[1] == "populate":
        game = GameManagement()
        connection = create_connection(DB_PATH)        
        game.create(connection)
        an = Analytics(game)
        an.show_challenges()
    
    elif sys.argv[1] == "test":
       date =  datetime.datetime(2021, 1, 1)
       print(is_holiday(date))

    
    else: print("Use python ./main <create|sim|plot|analyse|populate>")


    
    