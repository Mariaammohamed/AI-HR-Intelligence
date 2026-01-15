import sys

from fastapi import FastAPI, UploadFile, File
import fitz
import torch
from unsloth.chat_templates import get_chat_template
from pydantic import BaseModel

app = FastAPI()

def extract_text(file):
    doc = fitz.open(stream=file, filetype="pdf")
    return "".join([p.get_text() for p in doc])

@app.post("/parse")
async def parse_resume(file: UploadFile = File(...)):
    text = extract_text(await file.read())

    messages = [
        {"from":"human","value":"Extract structured resume data from this CV:\n\n" + text}
    ]

    inputs = tokenizer.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to("cuda")

    output = model.generate(
        input_ids=inputs,
        max_new_tokens=256,
        use_cache=True
    )

    result = tokenizer.decode(output[0], skip_special_tokens=True)

    return {"result": result}
    
