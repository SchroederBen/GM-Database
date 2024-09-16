import mysql.connector
from mysql.connector import Error


def get_players_with_injuries(conn):
    cursor = conn.cursor()
    try:
        select_players_with_injuries = """
        SELECT Player.PlayerID, Player.Name, Injury.Severity, Injury.date_of_injury, 
               Injury.date_of_return, Injured_Body_Part.Body_Part
        FROM Player
        JOIN Injury ON Player.PlayerID = Injury.PlayerID
        JOIN Injured_Body_Part ON Injury.InjuryID = Injured_Body_Part.InjuryID
        ORDER BY Injury.date_of_injury DESC
        """
        cursor.execute(select_players_with_injuries)
        results = cursor.fetchall()
        if results:
            print("Players with injuries:")
            for result in results:
                player_id, name, severity, date_of_injury, date_of_return, body_part = result
                print(f"Player ID: {player_id}, Name: {name}, Severity: {severity}, Date of Injury: {date_of_injury}, Expected Return: {date_of_return}, Injured Body Part: {body_part}")
        else:
            print("No injured players found.")
    except Error as e:
        print("Error occurred:", e)
    finally:
        cursor.close()
        
def record_injury(conn, injury_id, player_id, severity, date_of_injury, date_of_return, days_out, body_part=None):
    cursor = conn.cursor()
    try:
        # Insert into Injury table
        injury_insert = """
        INSERT INTO Injury (InjuryID, PlayerID, Severity, date_of_injury, date_of_return, days_out)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        injury_data = (injury_id, player_id, severity, date_of_injury, date_of_return, days_out)
        cursor.execute(injury_insert, injury_data)

        # Insert into Injured_Body_Part table if body_part is provided
        if body_part:
            body_part_insert = """
            INSERT INTO Injured_Body_Part (InjuryID, Body_Part)
            VALUES (%s, %s)
            """
            cursor.execute(body_part_insert, (injury_id, body_part))

        conn.commit()  # Commit the transaction
        print("Injury recorded successfully.")
    except Error as e:
        print("Error occurred:", e)
        conn.rollback()  # Rollback in case of error
    finally:
        cursor.close()

def update_player_stats(conn, player_id, assists, goals, points):
    cursor = conn.cursor()
    try:
        update_stats = """
        UPDATE Stats
        SET Assists = %s, Goals = %s, Points = %s
        WHERE PlayerID = %s
        """
        cursor.execute(update_stats, (player_id, assists, goals, points))
        conn.commit()
        print("Player stats updated successfully.")
    except Error as e:
        print("Error occurred:", e)
        conn.rollback()
    finally:
        cursor.close()


def add_player(conn, player_id, name, age, position):
    cursor = conn.cursor()
    try:
        insert_player = """
        INSERT INTO Player (PlayerID, Name, Age, Position)
        VALUES (%s, %s, %s, %s)
        """
        player_data = (player_id, name, age, position)
        cursor.execute(insert_player, player_data)
        conn.commit()
        print("Player added successfully.")
    except Error as e:
        print("Error occurred:", e)
        conn.rollback()
    finally:
        cursor.close()

def main():
    try:
        conn = mysql.connector.connect(host='localhost', user='root', password='Chickennoodle12', database='gm_database')
        print("Database connection established.")

        while True:
            print("\nMenu:")
            print("1. Record an Injury")
            print("2. Update Player Stats")
            print("3. Add Player")
            print("4. See Injured Players")
            print("5. Exit")
            choice = input("Enter your choice (1-5): ")

            if choice == '1':
                injury_id = int(input("Enter Injury ID: "))  # User enters the Injury ID
                player_id = int(input("Enter Player ID: "))
                severity = input("Enter Severity of the Injury: ")
                date_of_injury = input("Enter Date of Injury (YYYY-MM-DD): ")
                date_of_return = input("Enter Expected Return Date (YYYY-MM-DD): ")
                days_out = int(input("Enter Days Out: "))
                body_part = input("Enter Body Part Injured (Optional, press enter to skip): ")
                body_part = None if body_part == '' else body_part
                record_injury(conn, injury_id, player_id, severity, date_of_injury, date_of_return, days_out, body_part)

            elif choice == '2':
                player_id = int(input("Enter Player ID: "))
                assists = int(input("Enter Assists: "))
                goals = int(input("Enter Goals: "))
                points = int(input("Enter Points: "))
                update_player_stats(conn, player_id, assists, goals, points)

            elif choice == '3':
                player_id = int(input("Enter Player ID: "))
                name = input("Enter Player Name: ")
                age = int(input("Enter Player Age: "))
                position = input("Enter Player Position: ")
                add_player(conn, player_id, name, age, position)

            elif choice == '4':
                get_players_with_injuries(conn)

            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("Invalid choice, please choose from 1 to 3.")

    except mysql.connector.Error as e:
        print("Database connection failed:", e)
    finally:
        if conn.is_connected():
            conn.close()
            print("Database connection closed.")

if __name__ == "__main__":
    main()
