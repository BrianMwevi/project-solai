#!/usr/bin/env python

import asyncio

import websockets

users = set()


async def handler(websocket):
    users.add(websocket)
    print("User joined!", )
    async for message in websocket:
            pass
    #     websockets.broadcast(users, message)
    users.remove(websocket)


async def stocks_sock():
    async with websockets.serve(handler, "", 8001):
        await asyncio.Future()  # run forever


# if __name__ == "__main__":
#     asyncio.run(stocks_sock())
