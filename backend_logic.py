from fastapi import FastAPI
from pydantic import BaseModel
from base64 import b64decode
import fitz
import random

class Item(BaseModel):
    pdf_base64: str
   
    

appp = FastAPI()

@appp.post("/post-data")
async def handle_post(data: Item):
   pdf_64 = data.pdf_base64
   pdf_bytes = b64decode(pdf_64, validate=True)
   doc = fitz.open(stream=pdf_bytes, filetype="pdf")
   doc_info = {
        "file_size": len(pdf_bytes), 
        "page_count": doc.page_count,
        "pdf_base64": pdf_64
    }
   
   
   return {"message": f"PDF created{doc_info}"}    

@appp.post("/post-box")
async def post_box(data: Item):
   pdf_64 = data.pdf_base64
   pdf_bytes = b64decode(pdf_64, validate=True)
   doc = fitz.open(stream=pdf_bytes, filetype="pdf")
   random_x = random.randint(0, 100)
   random_y = random.randint(0, 100)
   doc_info = {
        "file_size": len(pdf_bytes), 
        "page_count": doc.page_count,
        # "pdf_base64": pdf_64,
        "bounding_box": {"x":random_x, "y":random_y, "width":200, "height":30},
        "pg_num": 1
    }
   
   return {"message": "PDF created", "info": doc_info}