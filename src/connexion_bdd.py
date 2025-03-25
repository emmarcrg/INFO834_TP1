import mysql.connector
import os

def get_db(logs_path=os.path.join("./logs_db.txt")):
    with open(logs_path, "r") as file:
        # Lire les 5 premières lignes du fichier (user/pwd/host/port/db)
        logs = file.readlines()
    
    db = mysql.connector.connect(
        user=logs[0][0:-1],
        password=logs[1][0:-1],
        host=logs[2][0:-1],
        port=logs[3][0:-1],
        database=logs[4][0:-1],
    )
    return db

def close_db(db):
    try:
        db.close()
        return 0
    except:
        return -1
    
def get_data(db, table_name, logs_path="logs_db.txt",columns="*",conditions=""):
    """
    Fonction pour récupérer les données d'une table
    conditions: doit être de la forme "WHERE condition1 (AND condition2...)"
    """
    cursor = db.cursor()
    query = f"SELECT {columns} FROM {table_name} {conditions}"
    cursor.execute(query)
    return cursor.fetchall()

    
if __name__ == "__main__":
    operation=""
    if operation == "connexion":
        db = get_db()
    elif operation == "fermeture":
        close_db(db)