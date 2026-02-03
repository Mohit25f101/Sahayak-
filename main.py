from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import base64

app = FastAPI()

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Hackathon-safe
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    user_command: str
    screenshot: str  # base64 image

@app.post("/analyze")
def analyze_page(data: AnalyzeRequest):
    """
    TEMP INTELLIGENCE (STABLE DEMO LOGIC)
    Replace with Vision AI after deployment is stable
    """

    command = data.user_command.lower()

    # VERY IMPORTANT:
    # Keep deterministic rules for demo reliability

    if "naam" in command or "name" in command:
        return {
            "action": "type",
            "selector": "input[name='name']",
            "value": "Mohit"
        }

    if "next" in command or "submit" in command:
        return {
            "action": "click",
            "selector": "button[type='submit']"
        }

    return {
        "action": "none",
        "selector": "",
        "value": ""
    }

@app.get("/")
def health_check():
    return {"status": "Sahayak backend running"}
