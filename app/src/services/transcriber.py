from fastapi import FastAPI, WebSocket, WebSocketDisconnect, APIRouter
from whisper import load_model
import asyncio
from concurrent.futures import ProcessPoolExecutor

app = FastAPI()
router = APIRouter()

transcriber_tags_metadata = [
    {
        "name": "Transcriber",
        "description": "Transcribe audio from a WebSocket connection.",
    }
]

# Cargamos el modelo de Whisper una vez
model = load_model("base")

async def transcribe_audio(websocket: WebSocket, queue: asyncio.Queue):
    while True:
        data = await queue.get()
        if data is None:
            break
        # Transcribimos el audio
        result = model.transcribe(data)
        # Enviamos la transcripción de vuelta al cliente
        await websocket.send_text(result['text'])
        queue.task_done()

@router.websocket("/ws/audio")
async def websocket_audio_endpoint(websocket: WebSocket):
    await websocket.accept()
    queue = asyncio.Queue()
    
    # Usamos un ProcessPoolExecutor para manejar la transcripción en un proceso separado
    loop = asyncio.get_event_loop()
    transcriber_task = loop.run_in_executor(None, transcribe_audio, websocket, queue)

    try:
        while True:
            data = await websocket.receive_bytes()
            await queue.put(data)
    except WebSocketDisconnect:
        print("Cliente desconectado")
        await queue.put(None)  # Indicamos al proceso que termine
        await transcriber_task  # Esperamos a que el transcriptor termine

app.include_router(router)
