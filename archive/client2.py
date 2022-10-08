from dataclasses import dataclass
import asyncio
from connexion import inscription, server

@dataclass
class MyInfo:
    name: str
    port: int
    matricule: str

async def othello(HOST_IP, PORT_IP, MyInfo):
    # se connecter au serveur de championnat
    inscriptionTask = asyncio.create_task(inscription(
        HOST_IP,
        PORT_IP,
        MyInfo.port,
        MyInfo.name,
        MyInfo.matricule)
    )
    await inscriptionTask

    # Lancer un serveur d'écoute
    serverTask = asyncio.create_task(server(MyInfo.port))
    await serverTask

ALi = MyInfo('ali', 5000, '1234')
asyncio.run(othello("127.0.0.1", 3000, ALi))
