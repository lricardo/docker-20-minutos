#!/usr/bin/env python

import asyncio
import websockets
import sys
import json
import enum

from aioconsole import ainput

class Color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

username = None
websocket = None

def colorized_str(msg, color):
    return color + msg + Color.END

async def register():
    global username
    global websocket

    username = input("What's your name? ")
    websocket = await websockets.connect('ws://0.0.0.0:8765')
    
    await websocket.send(username)
    print("> Registering user as: {}".format(username))
    
    greeting = await websocket.recv()
    print("< {}".format(greeting))

async def send():
    global username
    global websocket

    while True:
        if username and websocket:
            msg = await ainput('')
            
            if not msg:
                continue
                    
            await websocket.send(json.dumps({
                'from': username,
                'message': msg
            }))

        await asyncio.sleep(0.1)

async def receive():
    global websocket
    global username

    while True:
        if websocket:
            bundle = await websocket.recv()
            
            if not bundle:
                continue            
            
            bundle = json.loads(bundle)

            from_= bundle['from']
            msg = bundle['message']

            if msg:
                message = '{} sent: {}'.format(from_, msg)
                print(colorized_str(message, Color.BOLD))
        
        await asyncio.sleep(0.1)


loop = asyncio.get_event_loop()
tasks = asyncio.gather(register(), receive(), send())
loop.run_until_complete(tasks)
loop.run_forever()
