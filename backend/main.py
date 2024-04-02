from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
from fastapi import FastAPI, File, UploadFile, Form
import os

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


def process_with_llm(file_content:str, question:str):
    result = f"Processed {file_content} with question: {question}"
    return result
    

class Response(BaseModel):
    result: str | None

@app.post("/predict", response_model=Response)
async def predict(file: UploadFile = File(...), question: str = Form(...)) -> Any:
    # Save temporarily
    if not os.path.exists("temp"):
        os.makedirs("temp")

    with open(f"temp/{file.filename}", "wb") as f:
        f.write(await file.read())
        
    with open(f"temp/{file.filename}", "r") as f:
        file_content = f.read()
        
    print(file_content)
    result = process_with_llm(file_content, question)
    # result = f"Processed {file.filename} with question: {question}"
    print(result)
  
    return {"result": result}