from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any

# Load environment variables from .env file (if any)
load_dotenv()

class Response(BaseModel):
    result: str | None

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000"
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# @app.post("/predict", response_model = Response)
# def predict() -> Any:
  
#   #implement this code block
  
#   return {"result": "hello world!"}

@app.post("/predict", response_model=Response)
async def predict(file: UploadFile = File(...), question: str = Form(...)) -> Response:
    # Now, `file` is the uploaded file, and `question` is the associated question.
    
    # You can save the file temporarily if needed:
    with open(f"temp_{file.filename}", "wb") as buffer:
        buffer.write(file.file.read())
    
    # Here, you would process the file and the question.
    # For demonstration purposes, let's just echo the question.
    # In a real scenario, you'd replace this with logic to apply your model to the file's content.
    
    result = f"Processed {file.filename} with question: {question}"
    
    return {"result": result}
