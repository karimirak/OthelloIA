import socket
import json


def connexion(HOST, PORT):
    global connexion_avec_client, infos_connexion, connexion_principale

    connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_principale.bind((HOST, PORT))
    connexion_principale.listen(5)
    print("Le serveur écoute à présent sur le port {}".format(PORT))
    connexion_avec_client, infos_connexion = connexion_principale.accept()
    print(connexion_avec_client, infos_connexion)
    dialogue()

def envoyer(message):
    pong = {'response': 'pong'}
    json_message = json.dumps(pong)
    print(json_message)
    connexion_avec_client.send(json_message.encode())

def recevoir():
    msg_recu = connexion_avec_client.recv(1024)
    msg_recu=msg_recu.decode()
    return msg_recu

def dialogue():
    while True:
        msg_recu=recevoir()
        print(msg_recu)
        message = input("Entrez votre message: ")
        print(message)
        envoyer(message)

    print("Fermeture de la connexion")
    connexion_avec_client.close()
    connexion_principale.close()


connexion('localhost', 5000)