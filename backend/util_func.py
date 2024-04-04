import openai
import os
import tempfile
import pandas as pd
from fastapi import HTTPException
from docx import Document
from PyPDF2 import PdfReader
from fastapi import UploadFile, HTTPException
from docx2python import docx2python
import requests
import docx

API_Token = ''
API_URL = "https://api-inference.huggingface.co/models/openai-community/gpt2"
headers = {"Authorization": f"Bearer {API_Token}"}

def load_llm_model(prompt,API_URL,headers):
    response = requests.post(API_URL, headers=headers, json=prompt)
    return response.json()


def process_with_llm(file_content:str, question:str) ->str:
    try:

        prompt = {
	                "inputs": "Can you please let us know more details about your ",
        }

        output = load_llm_model(prompt=prompt, API_URL=API_URL,headers=headers)
        print('Output ',output)

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
    doc = docx.Document(file_path)
    fullText = []
    for para in doc.paragraphs:
        fullText.append(para.text)
    file_content = '\n'.join(fullText)
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
                
        # file_content = read_pdf(temp_file_path)

        print("Temporary file path:", temp_file_path)
        print("File type is:", type(file))
        print("File type:", file)
   
        if file.filename.endswith(".pdf"):
            file_content = read_pdf(file_path=temp_file_path)
        elif file.filename.endswith(".docx"):
            file_content = read_docx(temp_file_path)
        elif file.filename.endswith(".txt"):
            file_content = read_txt(temp_file_path)

        print("File content:", file_content)
            
    except Exception as e:
        print('Error:', e)
        raise HTTPException(status_code=500, detail="An error occurred in processing files")
    finally:
        if temp_file_path is not None and os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            
    return file_content
