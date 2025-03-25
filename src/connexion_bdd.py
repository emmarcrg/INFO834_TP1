import mysql.connector
import os

def get_db(logs_path=os.path.join("logs_db.txt")):
    with open(logs_path, "r") as file:
        # Lire les 4 premières lignes du fichier (user/pwd/host/port/db)
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