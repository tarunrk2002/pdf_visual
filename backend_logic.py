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
   block_list = []


   for i in range(doc.page_count):
       page = doc[i]
       print(i)

    #counting words
       text_words = page.get_text("words")
       word_count += len(text_words)

    #blocks
       blocks = page.get_text("blocks")   

    #counting lines 
       text_lines = page.get_text("text")
       line_count += len(text_lines.split("\n"))
    # trying something 
       lines = get_text_lines(page)
       lines_seperated = lines.split("\n\n")

    #loop for rectagles

       for block in blocks:
       
           highlight = fitz.Rect(block[0], block[1], block[2], block[3])
           page.draw_rect(highlight, color=(0, 1, 0), width=1)
           block_list.append((f"page number: {i}"))
           block_list.append(block)
           


       

           

   doc.save("output_with_bounding_box.pdf")
#    doc.close()

        



   doc_info = {
        "file_size": len(pdf_bytes), 
        "page_count": doc.page_count,
        # # "pdf_base64": pdf_64,
        # "bounding_box": {"x":random_x, "y":random_y, "width":200, "height":30},
        # "doc_height": doc_height,
        # "doc_width": doc_width,
        # "pg_num": 1,
        "line_count": line_count,
        
         "word_count": word_count,
        # "lines":lines,
        # "text_from_pdf":text_lines,
        # "lines_seperated_list":lines_seperated_list

        "blocks":block_list
    }
   
   return {"info": doc_info}
  



