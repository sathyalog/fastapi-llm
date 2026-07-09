import os

from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv
from fastapi.responses import StreamingResponse
load_dotenv(override=True)

app = FastAPI()
client = Groq(api_key=os.getenv("API_KEY"))

class PromptRequest(BaseModel):
    message: str

class PromptResponse(BaseModel):
    response: str
    model:str
    status: str

class RequestModel(BaseModel):
    name: str

def stream_response(message: str):
    stream = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": message}],
        stream=True
    )
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            yield content

@app.post("/generate-stream")
def generate(request: PromptRequest):
    return StreamingResponse(stream_response(request.message), media_type="text/event-stream")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("streaming:app", host="localhost", port=8000, reload=True)
