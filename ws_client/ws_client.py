import asyncio
import websockets
import json

async def listen_to_notifications(uri):
    async with websockets.connect(uri) as websocket:
        try:
            while True:
                message = await websocket.recv()
                notification = json.loads(message)
                print(f"status: {notification}")
        except websockets.ConnectionClosed:
            print("connection closed")

if __name__ == "__main__":
    uri = "ws://127.0.0.1:8000/ws"
    try:
        asyncio.run(listen_to_notifications(uri))
    except KeyboardInterrupt:
        pass
