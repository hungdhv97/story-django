import asyncio
import json

from channels.generic.websocket import AsyncWebsocketConsumer


class SubprocessConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']

        # Create an asynchronous subprocess
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT,
        )

        # Stream the output back to the WebSocket
        async for line in process.stdout:
            if not line:
                break
            await self.send(json.dumps({'message': line.decode('utf-8')}))

        await process.wait()

        await self.send(json.dumps({'commandCompleted': True}))
