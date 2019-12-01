import sqlite3
import sys
import time

# connect to the database
connection = sqlite3.connect("my_videogames.db")

# cursor
crsr = connection.cursor()

# create the table
crsr.execute("""CREATE TABLE IF NOT EXISTS videogames (name TEXT, platform TEXT, publisher TEXT, year_released INT);""")
connection.commit()


def add_game(name, platform, publisher, year):
    crsr.execute("""INSERT INTO videogames VALUES ("{}", "{}", "{}", "{}")""".format(name, platform, publisher, year))
    connection.commit()


def delete_game(game):
    crsr.execute("""DELETE FROM videogames WHERE name= "{}" """.format(game))
    connection.commit()
    print("\nGame successfully deleted!")


def sum_games():
    crsr.execute("""SELECT COUNT(*) FROM videogames""")
    game_sum = crsr.fetchone()[0]
    print("\nYou have", game_sum, "games.")


def avg_year():
    crsr.execute("""SELECT AVG(year_released) FROM videogames""")
    year_average = crsr.fetchone()[0]
    print("\nThe average release year of your games is", year_average, ".")


def list_games():
    for row in crsr.execute("""SELECT * FROM videogames"""):
        print("{} - {} - {} - {}".format(row[0], row[1], row[2], row[3]))


print("\nWelcome to the database!")
while True:
    print("\nYou can 'view', 'add', 'delete', or 'search' out your games. If you would like to exit, type 'exit'.")
    action = input("What would you like to do?   ").lower()

    # add a game
    if action == "add":
        game_name = input("What is the name of the game?   ")
        game_platform = input("What platform is it on?   ")
        game_publisher = input("Who published the game?   ")
        game_release_year = int(input("What year was it released?   "))
        crsr.execute("""SELECT name, platform FROM videogames""")
        records = crsr.fetchall()
        check = True
        for row in records:
            if game_name == row[0] and game_platform == row[1]:
                print(records)
                print("\nThat game is already in the database!")
                check = False
                break
        if check:
            add_game(game_name, game_platform, game_publisher, game_release_year)
            print("Game successfully added!")
            input("Press 'Enter' to continue.")

    # view the database
    elif action == "view":
        print("\nHere are your games:\n")
        list_games()
        sum_games()
        input("\n\nPress 'Enter' to continue.")
        print("Would you like to sort by:\n1. Name    2. Year    3. Publisher    4. Platform")
        print("Press any other key to go back.")
        choice = input()
        if choice == "1":
            print("")
            for row in crsr.execute("""SELECT * FROM videogames ORDER BY name"""):
                print("{} - {} - {} - {}".format(row[0], row[1], row[2], row[3]))
        elif choice == "2":
            print("")
            for row in crsr.execute("""SELECT * FROM videogames ORDER BY year_released"""):
                print("{} - {} - {} - {}".format(row[0], row[1], row[2], row[3]))
            avg_year()
        elif choice == "3":
            print("")
            for row in crsr.execute("""SELECT * FROM videogames ORDER BY publisher"""):
                print("{} - {} - {} - {}".format(row[0], row[1], row[2], row[3]))
        elif choice == "4":
            print("")
            for row in crsr.execute("""SELECT * FROM videogames ORDER BY platform"""):
                print("{} - {} - {} - {}".format(row[0], row[1], row[2], row[3]))

    # delete a game
    elif action == "delete":
        game = input("What game do you want to remove?   ")
        platform = input("What platform is it on?   ")
        crsr.execute("""SELECT name, platform FROM videogames""")
        records = crsr.fetchall()
        check = True
        loop = True
        no = False
        for row in records:
            if loop:
                if game == row[0] and platform == row[1]:
                    while True:
                        choice = input("Are you sure you want to delete " + game + "?  Y/N   ").lower()
                        if choice == "y":
                            delete_game(game)
                            check = False
                            loop = False
                            break
                        elif choice == "n":
                            check = False
                            no = True
                            loop = False
                            break
                        else:
                            print("I don't understand...")
        if check:
            if no:
                continue
            else:
                print("\nThat name isn't listed in the database.")

    # search for games
    elif action == "search":
        print("You can search by:\n1. Specific Name    2. Publisher    3. Platform    4. Year")
        print("Press any other key to return.")
        choice = input()
        if choice == "1":
            game = input("What game are you looking for?   ")
            crsr.execute("""SELECT name FROM videogames""")
            rows = crsr.fetchall()
            if (game,) in rows:
                for row in crsr.execute("""SELECT * FROM videogames WHERE name = "{}" """.format(game)):
                    print("")
                    print("{} - {} - {} - {}".format(row[0], row[1], row[2], row[3]))
            else:
                print("\nThat name isn't listed in the database.")
        elif choice == "2":
            publisher = input("What publisher?   ")
            crsr.execute("""SELECT publisher FROM videogames""")
            rows = crsr.fetchall()
            if (publisher,) in rows:
                for row in crsr.execute("""SELECT * FROM videogames WHERE publisher = "{}" """.format(publisher)):
                    print("{} - {} - {} - {}".format(row[0], row[1], row[2], row[3]))
            else:
                print("\nThat publisher isnt listed in the database.")
        elif choice == "3":
            platform = input("What platform?   ")
            crsr.execute("""SELECT platform FROM videogames""")
            rows = crsr.fetchall()
            if (platform,) in rows:
                for row in crsr.execute("""SELECT * FROM videogames WHERE platform = "{}" """.format(platform)):
                    print("{} - {} - {} - {}".format(row[0], row[1], row[2], row[3]))
            else:
                print("\nThat platform isn't listed in the database.")
        elif choice == "4":
            year = int(input("What year?   "))
            crsr.execute("""SELECT year_released FROM videogames""")
            rows = crsr.fetchall()
            if (year,) in rows:
                for row in crsr.execute("""SELECT * FROM videogames WHERE year_released = "{}" """.format(year)):
                    print("{} - {} - {} - {}".format(row[0], row[1], row[2], row[3]))
            else:
                print("\nThat year isn't listed in the database.")

    # quit the program
    elif action == "exit":
        while True:
            action = input("Are you sure you want to leave? Y/N   ").lower()
            if action == "y":
                print("Goodbye!")
                time.sleep(0.5)
                sys.exit(0)
            elif action == "n":
                break
            else:
                print("I cannot understand you...")
