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
   doc_height = doc[0].rect.height
   doc_width = doc[0].rect.width
   random_x = random.randint(0, 100)
   random_y = random.randint(0, 100)

   ## counting the total number of lines and words in the document

   line_count = 0
   word_count = 0
   for i in range(doc.page_count):
       page = doc[i]

    #counting for words
       text_words = page.get_text("words")
       word_count += len(text_words)

    #counting for lines 
       text_lines = page.get_text("text")
       line_count += len(text_lines.split("\n"))



   doc_info = {
        "file_size": len(pdf_bytes), 
        "page_count": doc.page_count,
        # "pdf_base64": pdf_64,
        "bounding_box": {"x":random_x, "y":random_y, "width":200, "height":30},
        "doc_height": doc_height,
        "doc_width": doc_width,
        "pg_num": 1,
        "line_count": line_count,
        
        "word_count": word_count,
        "text_from_pdf":text_lines,
    }
   
   return {"info": doc_info}