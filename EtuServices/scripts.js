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
        afficherAccueil(); // Redirection vers la page accueil
    };
    formulaire.appendChild(bouton);

    document.body.appendChild(formulaire);
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
