
import asyncio
from whisper import load_model

class Transcriber:
    def __init__(self):
        self.model = load_model("base")

    async def transcribe(self, file_path: str) -> str:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._transcribe_sync, file_path)

    def _transcribe_sync(self, file_path: str) -> str:
        result = self.model.transcribe(file_path)
        return result['text']