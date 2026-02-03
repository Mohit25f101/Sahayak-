from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import base64
import json

app = FastAPI(title="Sahayak API", version="2.0")

# Allow frontend to talk to backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production: ["https://yourdomain.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# In-memory storage for action history
action_history: List[dict] = []

class AnalyzeRequest(BaseModel):
    user_command: str
    screenshot: str  # base64 image
    url: Optional[str] = None

class ActionResponse(BaseModel):
    action: str
    selector: str
    value: str
    confidence: float
    timestamp: str
    explanation: str

class HistoryResponse(BaseModel):
    total: int
    actions: List[dict]

@app.post("/analyze", response_model=ActionResponse)
def analyze_page(data: AnalyzeRequest):
    """
    Analyzes user command and screenshot to determine automation action.
    
    Current implementation uses pattern matching.
    TODO: Replace with Vision AI (Claude/GPT-4V) for production.
    """
    
    command = data.user_command.lower()
    timestamp = datetime.now().isoformat()
    
    # Default response
    response = {
        "action": "none",
        "selector": "",
        "value": "",
        "confidence": 0.0,
        "timestamp": timestamp,
        "explanation": "Command not recognized"
    }
    
    # Pattern matching logic (replace with AI)
    if "naam" in command or "name" in command:
        # Extract value from command
        value = "Mohit"  # Default
        
        # Try to extract custom value
        if "with" in command:
            parts = command.split("with")
            if len(parts) > 1:
                # Extract text between "with" and next keyword
                value_part = parts[1].split("and")[0].strip()
                value = value_part
        
        response = {
            "action": "type",
            "selector": "input[name='name'], input[id='name'], input[placeholder*='name' i]",
            "value": value,
            "confidence": 0.85,
            "timestamp": timestamp,
            "explanation": f"Detected name field input with value: {value}"
        }
    
    elif "email" in command or "e-mail" in command:
        value = "user@example.com"
        
        if "with" in command:
            parts = command.split("with")
            if len(parts) > 1:
                value_part = parts[1].split("and")[0].strip()
                value = value_part
        
        response = {
            "action": "type",
            "selector": "input[type='email'], input[name='email'], input[id='email']",
            "value": value,
            "confidence": 0.90,
            "timestamp": timestamp,
            "explanation": f"Detected email field input with value: {value}"
        }
    
    elif "phone" in command or "mobile" in command:
        value = "1234567890"
        
        if "with" in command:
            parts = command.split("with")
            if len(parts) > 1:
                value_part = parts[1].split("and")[0].strip()
                value = value_part
        
        response = {
            "action": "type",
            "selector": "input[type='tel'], input[name*='phone' i], input[id*='phone' i]",
            "value": value,
            "confidence": 0.85,
            "timestamp": timestamp,
            "explanation": f"Detected phone field input with value: {value}"
        }
    
    elif any(word in command for word in ["next", "submit", "continue", "proceed"]):
        response = {
            "action": "click",
            "selector": "button[type='submit'], button:contains('Next'), button:contains('Submit'), input[type='submit']",
            "value": "",
            "confidence": 0.80,
            "timestamp": timestamp,
            "explanation": "Detected submit/next button click action"
        }
    
    elif "click" in command:
        # Extract button text if specified
        button_text = "button"
        if "button" in command:
            parts = command.split("button")
            if len(parts) > 0 and parts[0].strip():
                button_text = parts[0].replace("click", "").strip()
        
        response = {
            "action": "click",
            "selector": f"button:contains('{button_text}'), a:contains('{button_text}')",
            "value": "",
            "confidence": 0.75,
            "timestamp": timestamp,
            "explanation": f"Detected click action on element containing: {button_text}"
        }
    
    elif "scroll" in command:
        direction = "down"
        if "up" in command:
            direction = "up"
        
        response = {
            "action": "scroll",
            "selector": "window",
            "value": direction,
            "confidence": 0.95,
            "timestamp": timestamp,
            "explanation": f"Detected scroll {direction} action"
        }
    
    elif "wait" in command:
        duration = "2"  # Default 2 seconds
        
        # Try to extract number
        import re
        numbers = re.findall(r'\d+', command)
        if numbers:
            duration = numbers[0]
        
        response = {
            "action": "wait",
            "selector": "",
            "value": duration,
            "confidence": 1.0,
            "timestamp": timestamp,
            "explanation": f"Detected wait action for {duration} seconds"
        }
    
    # Store in history
    action_record = {
        "command": data.user_command,
        "url": data.url,
        "response": response,
        "timestamp": timestamp
    }
    action_history.append(action_record)
    
    # Keep only last 100 actions
    if len(action_history) > 100:
        action_history.pop(0)
    
    return response

@app.get("/history", response_model=HistoryResponse)
def get_history(limit: int = 20):
    """
    Retrieves action history.
    """
    recent_actions = action_history[-limit:] if len(action_history) > limit else action_history
    
    return {
        "total": len(action_history),
        "actions": list(reversed(recent_actions))  # Most recent first
    }

@app.delete("/history")
def clear_history():
    """
    Clears action history.
    """
    action_history.clear()
    return {"status": "success", "message": "History cleared"}

@app.post("/validate")
def validate_selector(selector: str):
    """
    Validates CSS selector syntax.
    """
    try:
        # Basic validation - in production use a proper CSS parser
        if not selector:
            return {"valid": False, "error": "Empty selector"}
        
        # Check for common issues
        if selector.count('[') != selector.count(']'):
            return {"valid": False, "error": "Mismatched brackets"}
        
        if selector.count('(') != selector.count(')'):
            return {"valid": False, "error": "Mismatched parentheses"}
        
        return {"valid": True, "selector": selector}
    
    except Exception as e:
        return {"valid": False, "error": str(e)}

@app.get("/stats")
def get_stats():
    """
    Returns usage statistics.
    """
    if not action_history:
        return {
            "total_actions": 0,
            "action_types": {},
            "success_rate": 0,
            "most_common_command": None
        }
    
    # Calculate statistics
    action_types = {}
    commands = []
    
    for record in action_history:
        action_type = record["response"]["action"]
        action_types[action_type] = action_types.get(action_type, 0) + 1
        commands.append(record["command"])
    
    # Most common command
    most_common = max(set(commands), key=commands.count) if commands else None
    
    return {
        "total_actions": len(action_history),
        "action_types": action_types,
        "success_rate": sum(1 for r in action_history if r["response"]["action"] != "none") / len(action_history) * 100,
        "most_common_command": most_common
    }

@app.get("/health")
def health_check():
    """
    Detailed health check endpoint.
    """
    return {
        "status": "healthy",
        "service": "Sahayak Automation API",
        "version": "2.0",
        "timestamp": datetime.now().isoformat(),
        "actions_in_history": len(action_history)
    }

@app.get("/")
def root():
    """
    API information endpoint.
    """
    return {
        "status": "Sahayak backend running",
        "version": "2.0",
        "endpoints": {
            "analyze": "POST /analyze - Analyze command and screenshot",
            "history": "GET /history?limit=20 - Get action history",
            "clear_history": "DELETE /history - Clear action history",
            "validate": "POST /validate - Validate CSS selector",
            "stats": "GET /stats - Get usage statistics",
            "health": "GET /health - Detailed health check"
        },
        "documentation": "/docs"
    }

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return {
        "error": exc.detail,
        "status_code": exc.status_code
    }

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return {
        "error": "Internal server error",
        "detail": str(exc)
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
