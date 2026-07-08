# FastAPI + Groq API Example

This project is a small FastAPI application that exposes a few demo endpoints and one AI-powered endpoint using the Groq Python SDK. It loads an API key from a `.env` file, accepts a prompt, sends it to a Groq chat model, and returns the generated response.

## What this project does

The app provides these endpoints:

- `GET /` returns a simple hello-world message.
- `GET /products` returns a sample list of products.
- `POST /generate` accepts a JSON body with a `message` field, sends that message to the Groq model, and returns the model output.

## Project file

Save your code in a file named `main.py`.

```python
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
    model: str
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
    return PromptResponse(
        response=response.choices[0].message.content,
        model=response.model,
        status="success"
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
```

## Project configuration with `uv`

You are using `uv`, so dependency management comes from your `pyproject.toml` file instead of `requirements.txt`.

Your project configuration is:

```toml
[project]
name = "fastapi-project"
version = "0.1.0"
description = "Add your description here"
readme = "README.md"
requires-python = ">=3.12"
dependencies = [
    "fastapi>=0.139.0",
    "groq>=1.5.0",
    "python-dotenv>=1.2.2",
    "uvicorn>=0.50.2",
]
```

This means `uv` will create and manage the virtual environment and install the dependencies listed in `pyproject.toml`.

## Libraries used

This project needs these libraries:

- `fastapi` — used to build the API and define routes like `GET /` and `POST /generate`.
- `groq` — used to call the Groq LLM API.
- `python-dotenv` — used to load the API key from the `.env` file.
- `uvicorn` — used to run the FastAPI app locally as an ASGI server.

## What `uvicorn` is and why it is used

`uvicorn` is a lightweight ASGI server for Python web applications.

FastAPI is not a web server by itself. FastAPI defines the application and routes, but something still needs to actually serve that app over HTTP on a host and port such as `http://localhost:8000`. That job is done by `uvicorn`.

In simple terms:

- FastAPI = your API application.
- Uvicorn = the server that runs the FastAPI application.

It is used because FastAPI is built on the ASGI standard, and Uvicorn is one of the most common ASGI servers for development and production-style Python APIs.

## How to create and use the virtual environment with `uv`

Since you are using `uv`, you do not need to manually create a virtual environment with `python -m venv` unless you want to. `uv` handles this nicely.

From your project folder, run:

```bash
uv sync
```

This will:

- create a virtual environment if needed,
- install the dependencies from `pyproject.toml`,
- keep the environment in sync with your project config.

In many setups, `uv` creates the environment in a `.venv` folder.

## How to activate the virtual environment

If you want to activate it manually:

### macOS / Linux

```bash
source .venv/bin/activate
```

### Windows PowerShell

```powershell
.venv\Scripts\Activate.ps1
```

After activation, you can run Python commands directly from that environment.

## Run without manual activation

A nice feature of `uv` is that you often do not need to activate the environment at all.

You can run commands like this:

```bash
uv run  main.py(i prefer this)
```

Or directly with Uvicorn:

```bash
uv run uvicorn main:app --host localhost --port 8000 --reload
```

This is usually the cleanest approach when using `uv`.

## Recommended way to run this project

Use this command from the project directory:

```bash
uv run uvicorn main:app --host localhost --port 8000 --reload
```

Why this is recommended:

- it uses the environment managed by `uv`,
- it runs the FastAPI app through Uvicorn,
- `--reload` restarts the server automatically when code changes.

You can also run:

```bash
uv run python main.py
```

That works because your code already contains:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
```

## Environment variables

Create a `.env` file in the same folder as `main.py`.

```env
API_KEY=your_groq_api_key_here
```

Important notes:

- The code uses `os.getenv("API_KEY")`, so the variable name must be exactly `API_KEY`.
- Do not commit your real `.env` file to GitHub.
- Add `.env` to `.gitignore`.

Example `.gitignore`:

```gitignore
.venv/
.env
__pycache__/
```

## How to test the API

Once the server is running, open these URLs or test with `curl`.

### 1. Root endpoint

```bash
curl http://localhost:8000/
```

Expected response:

```json
{"message":"Hello, World!"}
```

### 2. Products endpoint

```bash
curl http://localhost:8000/products
```

Expected response:

```json
{"products":["Product 1","Product 2","Product 3"]}
```

### 3. Generate endpoint

I personally use thunder client extension to test this /generate end point and here is the screenshot
![alt text](<Screenshot 2026-07-08 at 11.00.49 PM.png>)

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"message":"Write a one-line welcome message for my website"}'
```

Example response shape:

```json
{
  "response": "Welcome to our website — we're glad you're here!",
  "model": "llama-3.3-70b-versatile",
  "status": "success"
}
```

## Interactive API docs

FastAPI automatically provides docs when the server is running:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Notes about the code

- `PromptRequest` defines the incoming JSON body for `/generate`.
- `PromptResponse` defines the JSON structure returned by `/generate`.
- `RequestModel` is currently unused and can be removed if not needed.
- `load_dotenv(override=True)` loads values from `.env`.

## Suggested improvement

It is safer to validate the API key before creating the client. For example:

```python
api_key = os.getenv("API_KEY")
if not api_key:
    raise ValueError("API_KEY is missing. Add it to your .env file.")

client = Groq(api_key=api_key)
```

This helps avoid confusing runtime errors when the key is missing.
