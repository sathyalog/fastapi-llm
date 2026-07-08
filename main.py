from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class RequestModel(BaseModel):
    name: str

@app.get("/")
def show_msg():
    return {"message": "Hello, World!"}

@app.get("/products")
def get_products():
    return {"products": ["Product 1", "Product 2", "Product 3"]}

@app.post("/generate")
def generate(request: RequestModel):
    return f"Hello, {request.name}!"

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
