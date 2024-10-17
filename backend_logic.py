from fastapi import FastAPI
from pydantic import BaseModel
from base64 import b64decode
import fitz
import random
from pymupdf4llm.helpers.get_text_lines import get_text_lines
from fastapi.middleware.cors import CORSMiddleware
class Item(BaseModel):
    pdf_base64: str
   
    

appp = FastAPI()

#cors

accepting_frontend_urls = [
    "http://localhost:3000"
]

appp.add_middleware(
    CORSMiddleware,
    allow_origins=accepting_frontend_urls,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@appp.get("/")
async def root():
    return {"message": "Hello World"}
 

@appp.post("/post-data")
async def post_box(data: Item):
   pdf_64 = data.pdf_base64
   pdf_bytes = b64decode(pdf_64, validate=True)
   print("got the pdf")
   doc = fitz.open(stream=pdf_bytes, filetype="pdf")
  

   ## counting the total number of lines and words in the document

   line_count = 0
   word_count = 0
   lines_seperated_list = []
   block_list = []



   for i in range(doc.page_count):
       page = doc[i]
       

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
           block_list.append({"pageIndex": i, "top": block[1], "left": block[0], "width": block[2] - block[0], "height": block[3] - block[1], "text": block[4]})
           


       

           

   doc.save("output_with_bounding_box.pdf")
#    doc.close()

        
   


   doc_info = {
       
        
    }
   
   return {"block": block_list}
  



if __name__ == "__main__":
    import uvicorn as un
    un.run(appp, host="0.0.0.0", port=8000)


    #if you want to run from the terminal use this     uvicorn backend_logic:appp --reload
