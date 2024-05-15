from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from .services.transcriber_service import router as transcriber_router
from .services.conversations_service import router as conversation_router
from .services.conversations_service import conversation_tags_metadata as tags_conversation
from .services.transcriber_service import transcriber_tags_metadata

tags = tags_conversation + transcriber_tags_metadata


app = FastAPI(docs_url="/docs", redoc_url=None, openapi_tags=tags)

app.include_router(transcriber_router)
app.include_router(conversation_router)

@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@app.get("/")
async def root():
    return {"message": "Hello World"}

