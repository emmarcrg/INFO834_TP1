// Fonction pour envoyer une requête au serveur Flask
function appelerFlask(param) {
    fetch('http://127.0.0.1:5000/api/run', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ param: param }), // Envoyer un paramètre
    })
        .then(response => response.json())
        .then(data => {
            console.log(`Réponse du serveur Flask : ${data.result}`);
        })
        .catch(error => {
            console.error('Erreur lors de l\'appel au serveur Flask :', error);
        });
    
        // Appel à la route /api/reset_connections
    fetch('http://127.0.0.1:5000/api/reset_connections', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log(`Réinitialisation réussie pour l'utilisateur : ${username}`);
            } else {
                console.error(`Échec de la réinitialisation : ${data.message}`);
            }
        })
        .catch(error => {
            console.error('Erreur lors de la réinitialisation :', error);
        });
    
}

// Exemple d'appel de la fonction
appelerFlask('Bonjour Flask!');

// Fonction pour générer la page de login
function afficherLogin() {
    document.body.innerHTML = ''; // Efface le contenu existant

    const titre = document.createElement('h1');
    titre.textContent = 'Connexion';
    document.body.appendChild(titre);

    const formulaire = document.createElement('form');
    formulaire.style.display = 'flex';
    formulaire.style.flexDirection = 'column';

    const inputNom = document.createElement('input');
    inputNom.type = 'text';
    inputNom.placeholder = 'Nom d\'utilisateur';
    formulaire.appendChild(inputNom);

    const inputMotDePasse = document.createElement('input');
    inputMotDePasse.type = 'password';
    inputMotDePasse.placeholder = 'Mot de passe';
    formulaire.appendChild(inputMotDePasse);

    const bouton = document.createElement('button');
    bouton.textContent = 'Se connecter';
    
    bouton.onclick = (e) => {
        e.preventDefault();
        // Récupérer les valeurs des champs
        const username = inputNom.value;
        const password = inputMotDePasse.value;

        console.log(`Nom d'utilisateur : ${username}`);
        console.log(`Mot de passe : ${password}`);

        // Envoyer les données au serveur Flask
        envoyerConnexion(username, password);
    };
    formulaire.appendChild(bouton);

    document.body.appendChild(formulaire);
}

// Fonction pour envoyer les données de connexion au serveur Flask
function envoyerConnexion(username, password) {
    //console.log("Tentative d'envoyer les données")
    fetch('http://127.0.0.1:5000/api/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username: username, password: password }), // Envoyer les données
    })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Connexion réussie');
                afficherAccueil(); // Redirection vers la page d'accueil
            } else {
                console.error('Échec de la connexion :', data.message);
                alert('Échec de la connexion : ' + data.message);
            }
        })
        .catch(error => {
            console.error('Erreur lors de la connexion :', error);
        });
}

// Fonction pour générer la page d'accueil
function afficherAccueil() {
    document.body.innerHTML = ''; // Efface le contenu existant

    const titre = document.createElement('h1');
    titre.textContent = 'Accueil';
    document.body.appendChild(titre);

    const texte = document.createElement('p');
    texte.textContent = 'Bienvenue sur la page d\'accueil !';
    document.body.appendChild(texte);

    const bouton = document.createElement('button');
    bouton.textContent = 'Voir nos services';
    bouton.onclick = () => afficherServices(); // Redirection vers la page services
    document.body.appendChild(bouton);
}

// Fonction pour générer la page des services
function afficherServices() {
    document.body.innerHTML = ''; // Efface le contenu existant

    const titre = document.createElement('h1');
    titre.textContent = 'Services';
    document.body.appendChild(titre);

    const texte = document.createElement('p');
    texte.textContent = 'Découvrez nos services exclusifs !';
    document.body.appendChild(texte);

    const bouton = document.createElement('button');
    bouton.textContent = 'Retour au Login';
    bouton.onclick = () => afficherLogin(); // Redirection vers la page login
    document.body.appendChild(bouton);
}

// Afficher la page de login au chargement
afficherLogin();
