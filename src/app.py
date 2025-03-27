from flask import Flask, request, jsonify
from flask_cors import CORS as cors
import redis as rd

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

@app.route('/api/time', methods=['GET'])
def get_server_time():
    # Obtenir l'heure actuelle depuis Redis
    redis_time = client.time()  # Renvoie un tuple (seconds, microseconds)
    seconds, microseconds = redis_time

    # Calculer le timestamp en microsecondes
    timestamp_microseconds = seconds * 1_000_000 + microseconds

    # Convertir en un format lisible
    from datetime import datetime
    readable_time = datetime.fromtimestamp(seconds).strftime('%H:%M:%S')

    return jsonify({
        'timestamp_microseconds': timestamp_microseconds,
        'readable_time': readable_time
    })

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
    
    connections = client.get("user:jean.dupont@example.com:connections")
    print(int(connections))
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
                
                # Afficher le nombre de connexions
                print(f"Utilisateur {username} - Nombre de connexions : {connection_count}")
                
                return jsonify({
                    'success': True,
                    'message': 'Connexion réussie',
                    'connections': connection_count
                })
            else:
                return jsonify({'success': False, 'message': 'Mot de passe incorrect'}), 401
        else:
            return jsonify({'success': False, 'message': 'Utilisateur inconnu'}), 404


    
if __name__ == '__main__':
    app.run(debug=True)  # Lancer le serveur sur http://127.0.0.1:5000
    