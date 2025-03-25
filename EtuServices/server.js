const express = require('express');
const { spawn } = require('child_process');
const path = require('path');
const app = express();
const cors = require('cors');

// Activer CORS pour toutes les routes
app.use(cors());

// Servir les fichiers statiques (HTML, CSS, JS)
app.use(express.static(path.join(__dirname, 'EtuServices')));

// Route pour exécuter le script Python
app.get('/run-python', (req, res) => {
    const pythonProcess = spawn('python', ['./src/connexion_bdd.py', 'connexion']);
    let output = '';

    pythonProcess.stdout.on('data', (data) => {
        output += data.toString();
    });

    pythonProcess.on('close', (code) => {
        res.send(output);
    });
});

// Démarrer le serveur
app.listen(4000, () => console.log('Serveur démarré sur http://localhost:4000'));