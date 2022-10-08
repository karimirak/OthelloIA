import asyncio
from jsonStream import readJSON, writeJSON
from play import play


async def inscription(HOST_IP, PORT_IP, MyInfo):
    print('Connexion au serveur de jeu')
    reader, writer = await asyncio.open_connection(HOST_IP, PORT_IP)
    requet = {
        "request": "subscribe",
        "port": MyInfo.port,
        "name": MyInfo.name,
        "matricules": [f"{MyInfo.matricule}"]
    }
    await writeJSON(writer, requet)
    response = await readJSON(reader)
    writer.close()
    await writer.wait_closed()
    return response


async def server(PORT, alg):
    server = await asyncio.start_server(lambda r,w: dialogue(r, w, alg), '0.0.0.0', PORT)
    print(f"Le serveur écoute sur le port {PORT}, avec l'algorithme {alg} ")
    async with server:
        await server.serve_forever()


async def dialogue(reader, writer, alg):
    message = await readJSON(reader)
    request = message['request']
    print(message)
    if request == 'ping':
        await writeJSON(writer, {"response": "pong"})
    elif request == 'play':
        msg = play(message, alg)
        await writeJSON(writer, msg)
    writer.close()
    await writer.wait_closed()
