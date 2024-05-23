from fastapi import APIRouter, HTTPException
import ollama
from ..models.conversation import Conversation

router = APIRouter()

from ..models.conversation import Conversation

conversation_tags_metadata = [
    {
        "name": "Conversations",
        "description": "Chat with some models.",
    },
    {
        "name": "Models",
        "description": "Get list of models available."    
    }
       
]

@router.post("/conversation/", tags=["Conversations"])
async def npc_response(conversation: Conversation | None = Conversation(**{"role": "user", "content": "Hello"})):
    try:
        
        stream = ollama.chat(model='phi3', messages=[
        {
        'role': conversation.role,
        'content': conversation.content,
        'keep_alive:': '-1'
        },

    ])
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))
    
    print("stream", stream)
    return stream


@router.get("/models/", tags=["Models"])
async def get_models():
    return {"models": ollama.list()}


async def generate_response_from_model(transcription: str):
    try:
        stream = ollama.chat(model='phi3', messages=[
        {
        'role': 'user',
        'content': transcription,
        'keep_alive:': '-1'
        },

    ])
    except Exception as e: 
        raise HTTPException(status_code=500, detail=str(e))
    
    print("stream", stream)
    return stream['message']['content']
