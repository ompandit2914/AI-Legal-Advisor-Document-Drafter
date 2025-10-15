# api_server.py
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from crew import legal_assistant_crew
import os

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(title="AI Legal Assistant API", version="1.0")

# Enable CORS (important for frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # use ["https://your-lovable-app-url.com"] in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input schema
class LegalRequest(BaseModel):
    user_input: str

@app.get("/")
def home():
    return {"message": "AI Legal Assistant Backend Running ✅"}

@app.post("/analyze")
def analyze_legal_case(request: LegalRequest):
    """
    Takes a legal issue in plain English and returns
    IPC sections, precedents, and drafted output.
    """
    user_input = request.user_input.strip()

    if not user_input:
        return {"error": "Please provide a valid legal issue."}

    try:
        result = legal_assistant_crew.kickoff(inputs={"user_input": user_input})
        return {"success": True, "result": result}
    except Exception as e:
        return {"success": False, "error": str(e)}