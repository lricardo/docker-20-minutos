#!/usr/bin/env python

import asyncio
import websockets

users = []

async def serve(websocket, path):
    global users

    print(websocket)

    if websocket not in users:
        name = await websocket.recv()
        print("< {}".format(name))

        greeting = "Hello {}!".format(name)
        await websocket.send(greeting)
        print("> {}".format(greeting))
        users.append(websocket)
    
    while True:
        msg = await websocket.recv()
        for user in users:
            if user is not websocket:
                await user.send(msg)
            else:
                await user.send('')


start_server = websockets.serve(serve, '0.0.0.0', 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
