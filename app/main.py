from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from src.services.transcriber import router as transcriber_router
from src.services.conversations import router as conversation_router
from src.services.conversations import conversation_tags_metadata as tags_conversation
import uvicorn

PORT = 8000

app = FastAPI(docs_url="/docs", redoc_url=None)

app.include_router(transcriber_router)
app.include_router(conversation_router)


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="192.168.0.238", port=PORT)
    print(f"Swagger UI available at http://localhost:{PORT}/docs")
