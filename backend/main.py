from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
from util_func import process_with_llm, process_input_file
import openai

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

# Load OpenAI API key from environment
openai.api_key = os.getenv('OPENAI_API_KEY')

if openai.api_key is None:
    raise EnvironmentError("OpenAI API key is not set in the environment.")



class Response(BaseModel):
    result: str | None
    

@app.post("/predict", response_model=Response)
def predict(file: UploadFile = File(...), question: str = Form(...)) -> Any:
    
    # byte_obj = await file.read()
        
    file_content = process_input_file(file)
    
    print("ddddddddfj",file_content)
        
    result = str(process_with_llm(file_content, question))
    # result = f"Processed {file.filename} with question: {question}"
    print(result)
  
    return {"result": result}