import os

from fastapi import FastAPI
from pydantic import BaseModel
from groq import Groq
from dotenv import load_dotenv

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

@app.get("/")
def show_msg():
    return {"message": "Hello, World!"}

@app.get("/products")
def get_products():
    return {"products": ["Product 1", "Product 2", "Product 3"]}

@app.post("/generate")
def generate(request: PromptRequest):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": request.message}],
    )
    return PromptResponse(response=response.choices[0].message.content, model=response.model, status="success")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
