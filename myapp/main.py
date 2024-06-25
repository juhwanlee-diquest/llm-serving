from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from transformers import AutoTokenizer, AutoModelForCausalLM
from pydantic import BaseModel
import torch

app = FastAPI()

# Allow CORS
origins = [
    "*",  # Allow all origins (for testing purposes, specify your domains in production)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load the model and tokenizer
model_name = "beomi/Llama-3-KoEn-8B-Instruct-preview"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
model.eval()
model.to(device)

class QueryRequest(BaseModel):
    question: str

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/post/recommend")
def get_post(query: QueryRequest):
    if not isinstance(query.question, str):
        raise HTTPException(status_code=400, detail="Question must be a string")
    
    # Create the instruction for summarization
    instruct = f"""
    ###지시사항:
    다음 문장을 요약해.
    반드시 한국어로 써
    문장: {query.question}
    
    ###요약: 
    """
    
    inputs = tokenizer(
        instruct,
        return_tensors="pt",
        max_length=1024,
        truncation=True,
    ).to(device)
    
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=512,
            do_sample=True,
            temperature=0.5,
        )

    decoded_output = tokenizer.decode(outputs[0], skip_special_tokens=True)
    summary = decoded_output.split("###요약:")[1].strip()
    
    return {"response": summary}
