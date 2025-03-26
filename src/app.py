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
    
@app.route('/api/run', methods=['POST'])
def run_function():
    result = f"Connexion avec le serveru flask"
    return jsonify({'result': result})
    
@app.route('/api/login', methods=['POST'])
def login():
    print("On appelle bien login")
    # Récupérer les données envoyées par le frontend
    data = request.get_json()
    print("Le code python reçoit les données suivantes : ", data)
    username = data.get('username')
    password = data.get('password')
    
    if username in utilisateur['email'] :
        index = utilisateur['email'].index(username)
        if utilisateur['mdp'][index] == password:
            return jsonify({'success': True, 'message': 'Connexion réussie'})
        else:
            return jsonify({'success': False, 'message': 'Mot de passe incorrect'}), 401
    
if __name__ == '__main__':
    app.run(debug=True)  # Lancer le serveur sur http://127.0.0.1:5000
    
