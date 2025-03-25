const express = require('express');
const path = require('path');
const app = express();
const PORT = 3000;

// Middleware pour servir les fichiers statiques (JS)
app.use(express.static(path.join(__dirname)));

// Route principale
app.get('/', (req, res) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Lancer le serveur
app.listen(PORT, () => {
    console.log(`Serveur démarré sur http://localhost:${PORT}`);
});
