from flask import Flask, request, jsonify
from flask_cors import CORS as cors

app = Flask(__name__)
cors(app)

# Exemple de route pour exécuter une fonction Python
@app.route('/api/run', methods=['POST'])
def run_function():
    utilisateur = {
        "id" : [1, 2, 3], 
        "prenom" : ["Jean", "Anna", "Fabien"],
        "nom" : ["Dupont", "Dupont", "Josh"], 
        "email" : ["jean.dupont@example.com", "anna.dupont@example.com", "fabien.josh@example.com"],
        "mdp" : ["jedu", "nadu", "fajo"]
    }
    param = utilisateur.get('prenom')  # Extraction du paramètre 'param'
    
    # Logique Python
    result = f"Traitement du paramètre : {param}"
    
    # Retourne la réponse au front-end
    return jsonify({'result': result})

if __name__ == '__main__':
    app.run(debug=True)  # Lancer le serveur sur http://127.0.0.1:5000
