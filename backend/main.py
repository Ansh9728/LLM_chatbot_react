from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
from util_func import process_with_llm, process_input_file
from util_func import summarize_content
from util_func import clean_file_content
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


class Response(BaseModel):
    result: str | None
    
API_Token = os.getenv('HF_ACCESS_TOKEN')    
headers = {"Authorization": f"Bearer {API_Token}"}
summarize_api_url="https://api-inference.huggingface.co/models/Falconsai/text_summarization"


@app.post("/predict", response_model=Response)
def predict(file: UploadFile = File(...), question: str = Form(...)) -> Any:
    
    # byte_obj = await file.read()
        
    file_content = process_input_file(file)
    
    file_content = clean_file_content(file_content=file_content)
    
    summarize_prompt = {
        "inputs": f"{file_content}",
        "parameters": {
            "do_sample": False,
            "temperature":1,
            "max_length":1024
            },
    }
    
    try:
        summarize_file_content = summarize_content(file_content=summarize_prompt, API_URL=summarize_api_url, headers=headers)
        
        summarize_file_content = summarize_file_content[0]['summary_text']   
        
        result = process_with_llm(file_content=summarize_file_content, question=question)
        
        if result:
            result = result['answer']
            return {"result": result}
        
    except Exception as e:
        return f"Error : {e}"