from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import UploadedFile

class ProgressConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)
        username = data.get('username')

        if not username:
            await self.send(json.dumps({'error': 'Username is required.'}))
            return

        # Fetch file progress for the given username
        files = UploadedFile.objects.filter(user__username=username).values('file', 'status', 'updated_at')
        await self.send(json.dumps({
            'files': list(files)
        }))
