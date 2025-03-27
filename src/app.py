from flask import Flask, request, jsonify
from flask_cors import CORS as cors
import redis as rd
from datetime import datetime

app = Flask(__name__)
cors(app, resources={r"/*": {"origins": "http://localhost:3000"}}) # Permet de recevoir des requêtes de toutes les origines

utilisateur = {
        "id" : [1, 2, 3], 
        "prenom" : ["Jean", "Anna", "Fabien"],
        "nom" : ["Dupont", "Dupont", "Josh"], 
        "email" : ["jean.dupont@example.com", "anna.dupont@example.com", "fabien.josh@example.com"],
        "mdp" : ["jedu", "nadu", "fajo"]
    }

#Création du client Redis 
client = rd.Redis(
    host='localhost',
    port=6379,
    db=0  # The default Redis database index
)

print("Connexion au serveur : ")
print(client.ping())  # Test de la connexion

@app.route('/api/reset_connections', methods=['POST'])
def reset_connections():
    # Réinitialiser le compteur de connexions pour tous les utilisateurs
    for email in utilisateur['email']:
        user_key = f"user:{email}:connections"
        client.set(user_key, 0)  # Réinitialiser le compteur à 0
        print(f"Le compteur de connexions pour l'utilisateur {email} a été réinitialisé.")
    
    return jsonify({'success': True, 'message': 'Compteurs de connexions réinitialisés pour tous les utilisateurs'}), 200

@app.route('/api/run', methods=['POST'])
def run_function():
    result = f"Connexion avec le serveur flask"
    return jsonify({'result': result})
    
@app.route('/api/login', methods=['POST'])
def login():
    print("On appelle bien login")
    # Récupérer les données envoyées par le frontend
    data = request.get_json()
    print("Le code python reçoit les données suivantes : ", data)
    username = data.get('username')
    password = data.get('password')
    
    connections = client.get(f"user:{username}:connections")
    if int(connections) >= 10 : 
        return jsonify({'success': False, 'message': 'Trop de connexions pour cet utilisateur'}), 403
    else :
        if username in utilisateur['email']:
            index = utilisateur['email'].index(username)
            if utilisateur['mdp'][index] == password:
                # Incrémenter le compteur de connexions pour cet utilisateur
                user_key = f"user:{username}:connections"
                connection_count = client.incr(user_key)
                
                # Ajouter l'utilisateur à une liste globale des utilisateurs connectés
                client.lpush("connected_users", username)
                
                # Obtenir l'heure actuelle depuis Redis
                redis_time = client.time()  # Renvoie un tuple (seconds, microseconds)
                seconds, microseconds = redis_time
                
                # Convertir en un format lisible
                connection_time = datetime.fromtimestamp(seconds).strftime('%H:%M:%S')
                
                disconnection_time=datetime.fromtimestamp(seconds + 600).strftime('%H:%M:%S')
                
                # Stocker l'heure de connexion dans Redis
                log_entry = {
                    'username': username,
                    'connection_time': connection_time,
                    'disconnection_time': disconnection_time
                }
                client.lpush("connection_logs", str(log_entry))  # Ajouter l'entrée au début de la liste
                
                # Afficher le nombre de connexions et l'heure
                print(f"Utilisateur {username} - Nombre de connexions : {connection_count}")
                print(f"Heure de connexion : {connection_time} ; Heure de déconnexion : {disconnection_time}")
                
                return jsonify({
                    'success': True,
                    'message': 'Connexion réussie',
                    'connections': connection_count
                })
            else:
                return jsonify({'success': False, 'message': 'Mot de passe incorrect'}), 401
        else:
            return jsonify({'success': False, 'message': 'Utilisateur inconnu'}), 404

@app.route('/api/logout', methods=['POST'])
def logout():
    # Obtenir l'heure actuelle depuis Redis
    redis_time = client.time()  # Renvoie un tuple (seconds, microseconds)
    seconds, microseconds = redis_time
    actual_time = datetime.fromtimestamp(seconds).strftime('%H:%M:%S')
    
    print("On passe bien dans le logout")
    
    # Récupérer la liste des utilisateurs connectés
    connected_users = client.lrange("connected_users", 0, -1)  # Renvoie une liste d'utilisateurs
    print(connected_users)
    
    for user in connected_users:
        print("nous avons des users")
        user = user.decode()  # Décoder les noms d'utilisateur (bytes -> string)
        
        # Récupérer les logs de connexion
        logs = client.lrange("connection_logs", 0, -1)  # Récupérer tous les logs
        for log in logs:
            print("notre user a des logs")
            log_entry = eval(log.decode())  # Convertir la chaîne en dictionnaire
            
            # Vérifier si l'heure actuelle correspond à l'heure de déconnexion
            if log_entry.get('username') == user and log_entry.get('disconnection_time') <= actual_time:
                print(f"L'heure actuelle {actual_time} correspond à l'heure de déconnexion de l'utilisateur {user}.")
                
                # Décrémenter la clé utilisateur
                client.decr(f"user:{user}:connections")
                
                # Supprimer l'utilisateur de la liste connected_users
                client.lrem("connected_users", 1, user)
                
                # Supprimer l'entrée correspondante de connection_logs
                client.lrem("connection_logs", 1, str(log_entry))
                
                return jsonify({
                    'success': True,
                    'message': f"L'heure actuelle correspond à l'heure de déconnexion de l'utilisateur {user}."
                })
    
    # Si aucune correspondance n'est trouvée
    return jsonify({
        'success': False,
        'message': "Aucune correspondance trouvée pour l'heure actuelle."
    })
    
if __name__ == '__main__':
    app.run(debug=True)  # Lancer le serveur sur http://127.0.0.1:5000
    