import socket
import json
import time
import asyncio
from archive import server

HOST_IP = "127.0.0.1"
PORT_IP = 3000

print('Connexion au serveur de jeu')
while True:
   try:
      s = socket.socket()
      s.connect((HOST_IP , PORT_IP))
   except ConnectionRefusedError:
      print('Erreur : impossible de se connecter, reconnexion en cours')
      time.sleep(3)
   else:
      print('Connection établie avec le serveur du jeu')
      break

data = {
   "request": "subscribe",
   "port": 3333,
   "name": "ali",
   "matricules": ["12345"]
}
dataJson = json.dumps(data)
s.send(dataJson.encode())

data_recues = s.recv(512).decode()
replyJson = json.loads(data_recues)
if replyJson['response'] == 'ok':
   asyncio.run(server.main())

s.close()