# 🚀 Sahayak - AI Browser Automation Assistant

<p align="center">
  <strong>Automate your browser tasks using natural language commands and voice control</strong>
</p>

## ✨ Features

### Core Features
- 🎯 **Smart Element Detection** - AI automatically identifies form fields, buttons, and elements
- 🎤 **Voice Control** - Speak commands naturally using Web Speech API
- 📸 **Screenshot Analysis** - Visual context for better automation accuracy
- ⚡ **Real-time Execution** - Instant command processing and execution
- 📊 **Action History** - Complete log of all automation steps
- 🔄 **Continuous Mode** - Monitor and automate repetitively

### Advanced Features
- **Auto-Execute Mode** - Automatically run commands after screenshot capture
- **Keyboard Shortcuts** - Fast workflow with Ctrl+Enter, Ctrl+S, Ctrl+V
- **Multi-action Commands** - Chain multiple actions in one command
- **Visual Feedback** - Animated UI with real-time status indicators
- **Error Handling** - Graceful error messages and recovery
- **Responsive Design** - Works on desktop and tablet devices

## 🎨 UI Design

The frontend features a **cyber-utility aesthetic** with:
- Animated grid background
- Neon accent colors (cyan, magenta, yellow)
- Custom fonts: Orbitron (headers) + JetBrains Mono (body)
- Smooth animations and hover effects
- Dark theme optimized for long usage
- Glowing orb ambient effect

## 📋 Prerequisites

- Python 3.8+
- Modern web browser (Chrome/Firefox/Edge)
- Microphone (for voice commands)

## 🛠️ Installation

### Step 1: Install Backend Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Start the Backend Server

```bash
uvicorn main:app --reload
```

The backend will start on `http://localhost:8000`

### Step 3: Open the Frontend

Simply open `index.html` in your web browser:

```bash
# On Mac/Linux
open index.html

# On Windows
start index.html

# Or just double-click the file
```

## 🎯 How to Use

### Basic Usage

1. **Enter Target URL**
   - Type the website URL you want to automate
   - Example: `https://forms.google.com/myform`

2. **Capture Screenshot**
   - Click "📸 Capture" button or press `Ctrl+S`
   - This gives AI visual context about the page

3. **Enter Command**
   - Type your command in plain English
   - Examples:
     - "Fill naam field with Mohit"
     - "Click the submit button"
     - "Fill naam with John and click next"

4. **Execute**
   - Click "⚡ Execute" or press `Ctrl+Enter`
   - Watch the action log for results

### Voice Commands

1. Click "🎤 Voice" button or press `Ctrl+V`
2. Speak your command clearly
3. Command will appear in text field
4. Click Execute or enable Auto-execute

### Advanced Options

**Auto-execute on capture** 
- Enable this to automatically run commands after taking a screenshot
- Great for repetitive workflows

**Continuous monitoring**
- Keep system ready for next command
- Auto-clears command field after execution
- Perfect for multi-step automation

## 💡 Example Commands

### Simple Commands
```
Fill naam with Mohit
Click submit button
Type "hello@example.com" in email field
```

### Complex Commands
```
Fill naam with Mohit and click next button
Enter my email and submit the form
Fill all fields and click submit
```

### Field Name Detection
The AI detects fields by:
- Name attribute
- ID attribute
- Placeholder text
- Label text
- Nearby text

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+Enter` | Execute command |
| `Ctrl+S` | Capture screenshot |
| `Ctrl+V` | Toggle voice recording |
| `Ctrl+L` | Focus URL field |

## 🔧 Configuration

### Changing Backend URL

If your backend runs on a different port, update the `API_URL` in `index.html`:

```javascript
const API_URL = 'http://localhost:8000'; // Change this
```

### CORS Configuration

The backend is configured with open CORS for development:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**For Production**: Replace `["*"]` with your specific domain:
```python
allow_origins=["https://yourdomain.com"]
```

## 🚀 Extending Functionality

### Adding Vision AI

The current backend uses deterministic rules. To add real AI:

1. **Install Claude API or OpenAI**
```bash
pip install anthropic
# or
pip install openai
```

2. **Update `main.py`**
```python
from anthropic import Anthropic

client = Anthropic(api_key="your-api-key")

@app.post("/analyze")
def analyze_page(data: AnalyzeRequest):
    # Decode screenshot
    image_data = base64.b64decode(data.screenshot)
    
    # Call Claude Vision
    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": data.screenshot,
                    },
                },
                {
                    "type": "text",
                    "text": f"User command: {data.user_command}\n\nAnalyze this webpage and return JSON with: action (type/click/none), selector (CSS selector), value (text to type)"
                }
            ],
        }]
    )
    
    # Parse response and return
    return parse_ai_response(message.content)
```

### Adding Browser Automation

To actually control the browser:

1. **Install Playwright or Selenium**
```bash
pip install playwright
playwright install
```

2. **Add automation endpoint**
```python
from playwright.async_api import async_playwright

@app.post("/execute")
async def execute_action(action_data: dict):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(action_data["url"])
        
        if action_data["action"] == "type":
            await page.fill(action_data["selector"], action_data["value"])
        elif action_data["action"] == "click":
            await page.click(action_data["selector"])
        
        await browser.close()
        return {"status": "success"}
```

### Custom Action Types

Add more action types in backend:

```python
# In analyze_page function
if "scroll" in command:
    return {"action": "scroll", "direction": "down"}

if "wait" in command:
    return {"action": "wait", "duration": 2}

if "screenshot" in command:
    return {"action": "screenshot", "filename": "result.png"}
```

## 🐛 Troubleshooting

### Backend Not Connecting
```
Error: Backend offline
```
**Solution**: Ensure backend is running on port 8000
```bash
uvicorn main:app --reload --port 8000
```

### Voice Not Working
```
Error: Voice recognition not supported
```
**Solution**: 
- Use Chrome/Edge browser (best support)
- Allow microphone permissions
- Use HTTPS in production

### CORS Errors
```
Error: CORS policy blocked
```
**Solution**: Check backend CORS settings or use `--reload` flag

### Screenshot Not Capturing
**Note**: Current implementation uses mock screenshots. For real screenshots:
- Use browser extension
- Use Playwright/Puppeteer
- Use desktop automation tools

## 📊 API Documentation

### POST `/analyze`
Analyzes screenshot and command to determine action

**Request:**
```json
{
  "user_command": "Fill naam with Mohit",
  "screenshot": "base64_encoded_image"
}
```

**Response:**
```json
{
  "action": "type",
  "selector": "input[name='name']",
  "value": "Mohit"
}
```

### GET `/`
Health check endpoint

**Response:**
```json
{
  "status": "Sahayak backend running"
}
```

## 🎓 Best Practices

1. **Be Specific** - "Click submit button" is better than "click button"
2. **Use Field Names** - Reference fields by their label or name
3. **Capture First** - Always capture screenshot before executing
4. **Test Commands** - Start with simple commands before complex ones
5. **Review Logs** - Check action log for debugging

## 🔐 Security Notes

⚠️ **Important for Production:**

1. **API Keys**: Never expose API keys in frontend code
2. **CORS**: Restrict origins to your domain only
3. **Input Validation**: Validate all user inputs on backend
4. **Rate Limiting**: Add rate limiting to prevent abuse
5. **Authentication**: Add user authentication for production

## 🤝 Contributing

Want to improve Sahayak?

1. Add real vision AI (Claude/GPT-4V)
2. Implement actual browser automation
3. Add more action types
4. Improve UI/UX
5. Add test suite
6. Create browser extension

## 📝 License

MIT License - feel free to use in your projects!

## 🙏 Acknowledgments

- FastAPI for the backend framework
- Web Speech API for voice recognition
- Orbitron & JetBrains Mono fonts
- The open-source community

---

<p align="center">
  Made with ⚡ for automating the web
</p>