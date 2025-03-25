const http = require('http');

const hostname = '127.0.0.1';
const port = 3000;

const server = http.createServer((req, res) => {
  res.statusCode = 200;
  res.setHeader('Content-Type', 'text/html');
  res.end('<!DOCTYPE html><html><head><title>Ma Page Web</title></head><body><h1>Bienvenue sur ma page web!</h1><p>Ceci est une page web simple créée avec Node.js.</p></body></html>');
});

server.listen(port, hostname, () => {
  console.log(`Le serveur tourne à l'adresse http://${hostname}:${port}/`);
});
