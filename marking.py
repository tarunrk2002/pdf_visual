#imports

import json
import fitz 
from flask import Flask,render_template,request,send_file

 


pdf_path = "pdf3.pdf"  
doc = fitz.open(pdf_path)


search_text = "kush"


page = doc[0] 


text_instances = page.search_for(search_text)

print(f"this is the text instances {text_instances}")


for i in text_instances:
    
    highlight = fitz.Rect(i)
    page.draw_rect(highlight, color=(0, 1, 0), width=1) 


output_pdf_path = "output_with_bounding_box.pdf"
doc.save(output_pdf_path)

doc.close()

print(f"Bounding box added and saved to {output_pdf_path}")
