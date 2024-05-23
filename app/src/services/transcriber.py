from fastapi import WebSocket, WebSocketDisconnect, APIRouter
import asyncio
from whisper import load_model
import tempfile
import time
from scipy.io.wavfile import write
import numpy as np
from .conversations import generate_response_from_model

router = APIRouter()

async def transcribe_audio(data: bytes):
    print("entre")
    model = load_model("base")  
    
    
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        audio_array = np.frombuffer(data, dtype=np.int16)
        write(tmp.name, 48000, audio_array)  
        tmp.flush()
        print("Archivo temporal creado")

        
        # with open("temporal.wav", "wb") as f:
        #     f.write(tmp.name)
        print("Archivo temporal guardado")
        start_time = time.time()
        try:
            transcription = model.transcribe(tmp.name)
            print(type(transcription), transcription)
        except Exception as e:
            print(f"Error durante la transcripción: {e}")
            transcription = "Transcripción falló debido a un error"
        
        end_time = time.time()
        print(f"Transcripción recibida: {transcription}")
        print(f"Tiempo de transcripción: {end_time - start_time:.2f} segundos")
        
        return transcription

from fastapi import WebSocket, WebSocketDisconnect, APIRouter

router = APIRouter()

@router.websocket("/ws/audio")
async def websocket_audio_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive()
            print(type(data))
            print(data.keys())
            print(data["type"], data["bytes"][:10])

            if data["type"] == "websocket.receive":
                audio_bytes = data["bytes"]
                try:
                    if isinstance(audio_bytes, (bytes, bytearray)):
                        transcription = await transcribe_audio(audio_bytes)
                        print(f"Transcription: {transcription}")
                        model_response = await generate_response_from_model(transcription['text'])

                        print(f"Sending model response: {model_response}")
                        await websocket.send_text(model_response)
                    else:
                        raise ValueError("El dato recibido no es de tipo bytes")
                except Exception as e:
                    print(f"Error al procesar audio: {e}")
                    await websocket.send_text(f"Error al procesar audio: {e}")
            elif data["type"] == "websocket.disconnect":
                code = data["code"]
                print(f"Cliente desconectado con código: {code}")
                break
            else:
                print(f"Datos recibidos no contienen 'bytes': {data['type']}")
    except WebSocketDisconnect:
        print("Cliente desconectado")
    except Exception as e:
        print(f"Error en WebSocket: {e}")
    finally:
        try:
            if not websocket.client_state.closed:
                await websocket.close()
        except Exception as e:
            print(f"Error al cerrar WebSocket: {e}")

