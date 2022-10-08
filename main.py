from dataclasses import dataclass
import asyncio
from connexion import inscription, server

@dataclass
class MyInfo:
    name: str
    port: int
    matricule: str
    alg : str

async def othello(MyInfo):
    # se connecter au serveur de championnat
    HOST_IP = 'localhost' #'10.12.12.63'
    PORT_IP = 3000
    inscriptionTask = asyncio.create_task(inscription(
        HOST_IP,
        PORT_IP,
        MyInfo
    )
    )
    await inscriptionTask

    # Lancer un serveur d'écoute
    serverTask = asyncio.create_task(server(MyInfo.port, MyInfo.alg))
    await serverTask


karim = MyInfo('karim', 4000, '5845', 'random')
Ali = MyInfo('Ali', 4001, '87455','minimax')
Husein = MyInfo('Husein', 3004, '6352','weight')

loop = asyncio.get_event_loop()
loop.run_until_complete(
    asyncio.gather(
    othello(karim),
    othello(Husein),
    othello(Ali),
))