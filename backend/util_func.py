import re
import os
import string
import tempfile
import pandas as pd
from fastapi import HTTPException
from docx import Document
from PyPDF2 import PdfReader
from fastapi import UploadFile, HTTPException
from docx2python import docx2python
import requests
import docx2txt
from dotenv import load_dotenv
import nltk
nltk.download("stopwords")

load_dotenv()

API_Token = os.getenv('HF_ACCESS_TOKEN')

API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"

headers = {"Authorization": f"Bearer {API_Token}"}

def load_llm_model(prompt,API_URL,headers):
    response = requests.post(API_URL, headers=headers, json=prompt)
    return response.json()


def summarize_content(file_content,API_URL ,headers):
    summarize_res = load_llm_model(prompt=file_content, API_URL=API_URL,headers=headers)
    return summarize_res


def process_with_llm(file_content:str, question:str) ->str:
    try:
        prompt = {
        "inputs": {
            "question": f"{question}",
            "context": f"{file_content}",
            "parameters": {
            "max_seq_len":512
            },
        }      
        }

        output = load_llm_model(prompt=prompt, API_URL=API_URL,headers=headers)

        return output

    except Exception as e:
        print("Error in llm process with llm")
        raise HTTPException(status_code=500, detail="Error during handling the llm")
    

def read_pdf(file_path):
    text = ''
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PdfReader(pdf_file)
        for page_num in range(len(pdf_reader.pages)):
            text += pdf_reader.pages[page_num].extract_text()

    file_content = text
    return file_content


def read_docx(file_path):
    
    file_content = docx2txt.process(file_path)   
    
    return file_content


def read_txt(file_path):
    with open(file_path, 'r') as f:
        file_content = f.read()

    return file_content


def process_input_file(file: UploadFile) -> str:
    temp_file_path = None
    file_content = None
    
    try:
        if isinstance(file, str):
            # If the file is already read, no need to read again
            temp_file_path = file
        else:
            # Save the file to a temporary location
            with tempfile.NamedTemporaryFile(delete=False, mode="wb") as temp_file:
                temp_file.write(file.file.read())
                temp_file_path = temp_file.name
                
   
        if file.filename.endswith(".pdf"):
            file_content = read_pdf(file_path=temp_file_path)
        elif file.filename.endswith(".docx"):
            file_content = read_docx(temp_file_path)
        elif file.filename.endswith(".txt"):
            file_content = read_txt(temp_file_path)
   
   
    except Exception as e:
        print('Error:', e)
        raise HTTPException(status_code=500, detail="An error occurred in processing files")
    finally:
        if temp_file_path is not None and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
    return file_content


def clean_file_content(file_content: str) ->str:
    
    cleaned_content = file_content.strip()

    cleaned_content = re.sub(r'\s+', ' ', cleaned_content)
    
    cleaned_content = " ".join(cleaned_content.split())
    cleaned_content = "".join(
        [char for char in cleaned_content if char not in string.punctuation]
    )
    words = cleaned_content.split()  # Tokenize the text
    
    stop_words = nltk.corpus.stopwords.words("english")
    
    words = [word for word in words if word.lower() not in stop_words]
    
    cleaned_content = " ".join(words)
    
    return cleaned_content