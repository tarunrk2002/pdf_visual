from fastapi import FastAPI
from pydantic import BaseModel
from base64 import b64decode
import fitz
import random
from pymupdf4llm.helpers.get_text_lines import get_text_lines

class Item(BaseModel):
    pdf_base64: str
   
    

appp = FastAPI()


 

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
   lines_seperated_list = []


   for i in range(doc.page_count):
       page = doc[i]

    #counting words
       text_words = page.get_text("words")
       word_count += len(text_words)

    #counting lines 
       text_lines = page.get_text("text")
       line_count += len(text_lines.split("\n"))
    # trying something 
       lines = get_text_lines(page)
       lines_seperated = lines.split("\n\n")

       for line in lines_seperated:
           lines_seperated_list.append(line)
           highlight = fitz.Rect(line)
           page.draw_rect(highlight, color=(0, 1, 0), width=1) 

       words = page.get_text("words")  # list of words with their bounding boxes
       for w in words:
            word_rect = fitz.Rect(w[:4])  # The first four elements in the word are the coordinates
            page.draw_rect(word_rect, color=(0, 1, 0), width=1)

           

   doc.save("output_with_bounding_box.pdf")
   doc.close()

        



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
        "lines":lines,
        "text_from_pdf":text_lines,
        "lines_seperated_list":lines_seperated_list
    }
   
   return {"info": doc_info}

