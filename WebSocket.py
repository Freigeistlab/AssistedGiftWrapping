import asyncio

import websockets
from threading import Thread, Timer

USERS = set()


class WebSocket(Thread):

    def __init__(self, orchestrator):
        super().__init__()
        self.orchestrator = orchestrator

    async def serve(self, websocket, path):
        await self.register(websocket)
        await self.send_message(self.orchestrator.get_current_message())
        while True:
            await asyncio.sleep(0.1)

    async def register(self, websocket):

        # send message corresponding to current state to the clients
        USERS.add(websocket)

    async def unregister(self,websocket):
        USERS.remove(websocket)

    def send_current_state(self):
        t = Timer(0.5, self.send_state_async)
        t.start()

    def send_state_async(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        task = loop.create_task(self.send_message(self.orchestrator.get_current_message()))
        loop.run_until_complete(task)

    async def send_message(self, message):
        if USERS:
            print("Sending message to users ", message)
            [await user.send(message) for user in USERS]
            print("message sent")

    def run(self):
        self.ws_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.ws_loop)
        ws = websockets.serve(self.serve, '', 5678)
        self.ws_loop.run_until_complete(ws)
        self.ws_loop.run_forever()
        return