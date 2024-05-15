from fastapi import APIRouter, UploadFile, File, HTTPException
from ..models.transcriber_model import Transcriber

router = APIRouter()
transcriber_service = Transcriber()

transcriber_tags_metadata = [
    {
        "name": "transcriber",
        "description": "Get Responses from models.",
    }
]

@router.post("/transcribe/", tags=["transcriber"])
async def transcribe_audio(file: UploadFile = File(...), tags=["transcriber"]):
    try:
        temp_file_path = f"temp_{file.filename}"
        with open(temp_file_path, "wb") as f:
            f.write(await file.read())

        transcription = await transcriber_service.transcribe(temp_file_path)
        return {"filename": file.filename, "transcription": transcription}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        import os
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)

