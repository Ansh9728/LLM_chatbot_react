from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Any
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
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

# Define a function to process with the language model
def process_with_llm(file_content: str, question: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a chatbot."},
                {"role": "user", "content": question},
                {"role": "assistant", "content": file_content},
            ],
            max_tokens=150,
            temperature=0.7
        )
        return response['choices'][0].message.content
    except openai.OpenAIError as e:
        print('erros is ',e)
        raise HTTPException(status_code=500, detail="An error occurred while generating the Chatbot response.")


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
        
    result = process_with_llm(file_content, question)
    # result = f"Processed {file.filename} with question: {question}"
    print(result)
  
    return {"result": result}