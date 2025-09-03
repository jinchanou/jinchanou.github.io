from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import openai
import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

app = FastAPI(title="TransNative API", description="Translation API using LLMs for natural English translations")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8001", "http://100.65.26.67:8001"],  # Add your local IP here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Serve static files (HTML, CSS, JS)
app.mount("/static", StaticFiles(directory="."), name="static")

@app.get("/")
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()
    return HTMLResponse(content=content)

class TranslationRequest(BaseModel):
    text: str
    context: str = None

class TranslationResponse(BaseModel):
    translations: list[str]

def translate_with_deepseek(text: str, context: str = None) -> list[str]:
    """Translate Chinese text to natural English using DeepSeek API"""
    try:
        # Get API key and endpoint from environment variables
        api_key = os.getenv("DEEPSEEK_API_KEY")
        endpoint = os.getenv("DEEPSEEK_ENDPOINT", "https://api.deepseek.com/chat/completions")
        model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        
        # Enhanced prompt for more natural translations
        if context:
            prompt = f"""You are a professional translator who specializes in translating Chinese to natural, authentic American English.
            
            Requirements:
            1. Provide 3-5 different translation options
            2. Translations must be natural and authentic, but not overly casual or artificial
            3. If applicable, include commonly used slang with a note
            4. If there are differences in usage context (formal/informal) or audience, please indicate
            5. Format: Each translation on a new line, followed by context notes in parentheses if needed
            6. Do not include explanations or numbering, only the translations and optional notes
            7. IMPORTANT: The translation should be appropriate for the context: {context}
            
            Chinese: {text}
            English:"""
        else:
            prompt = f"""You are a professional translator who specializes in translating Chinese to natural, authentic American English.
            
            Requirements:
            1. Provide 3-5 different translation options
            2. Translations must be natural and authentic, but not overly casual or artificial
            3. If applicable, include commonly used slang with a note
            4. If there are differences in usage context (formal/informal) or audience, please indicate
            5. Format: Each translation on a new line, followed by context notes in parentheses if needed
            6. Do not include explanations or numbering, only the translations and optional notes
            
            Chinese: {text}
            English:"""
        
        # Prepare request payload
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 300,
            "temperature": 0.7
        }
        
        # Set headers
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Make API request
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        
        # Parse response
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        # Split the response into lines and clean them
        translations = content.strip().split('\n')
        translations = [t.strip() for t in translations if t.strip()]
        return translations
    except Exception as e:
        print(f"Error in DeepSeek translation: {e}")
        return []

def translate_with_deepseek_pro(text: str, context: str = None) -> list[str]:
    """Translate Chinese text to natural English using DeepSeek Pro API as fallback"""
    try:
        # Get API key and endpoint from environment variables
        api_key = os.getenv("DEEPSEEK_API_KEY")
        endpoint = os.getenv("DEEPSEEK_ENDPOINT", "https://api.deepseek.com/chat/completions")
        model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")
        
        # Enhanced prompt for more natural translations
        if context:
            prompt = f"""You are a professional translator who specializes in translating Chinese to natural, authentic American English.
            
            Requirements:
            1. Provide 3-5 different translation options
            2. Translations must be natural and authentic, but not overly casual or artificial
            3. If applicable, include commonly used slang with a note
            4. If there are differences in usage context (formal/informal) or audience, please indicate
            5. Format: Each translation on a new line, followed by context notes in parentheses if needed
            6. Do not include explanations or numbering, only the translations and optional notes
            7. IMPORTANT: The translation should be appropriate for the context: {context}
            
            Chinese: {text}
            English:"""
        else:
            prompt = f"""You are a professional translator who specializes in translating Chinese to natural, authentic American English.
            
            Requirements:
            1. Provide 3-5 different translation options
            2. Translations must be natural and authentic, but not overly casual or artificial
            3. If applicable, include commonly used slang with a note
            4. If there are differences in usage context (formal/informal) or audience, please indicate
            5. Format: Each translation on a new line, followed by context notes in parentheses if needed
            6. Do not include explanations or numbering, only the translations and optional notes
            
            Chinese: {text}
            English:"""
        
        # Prepare request payload with DeepSeek Pro model
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "max_tokens": 300,
            "temperature": 0.7
        }
        
        # Set headers
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        # Make API request
        response = requests.post(endpoint, json=payload, headers=headers)
        response.raise_for_status()
        
        # Parse response
        result = response.json()
        content = result["choices"][0]["message"]["content"]
        
        # Split the response into lines and clean them
        translations = content.strip().split('\n')
        translations = [t.strip() for t in translations if t.strip()]
        return translations
    except Exception as e:
        print(f"Error in DeepSeek Pro translation: {e}")
        return []

@app.post("/translate", response_model=TranslationResponse)
async def translate(request: TranslationRequest):
    """Translate Chinese text to multiple natural English options"""
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text is required")
    
    # Try DeepSeek translation first
    translations = translate_with_deepseek(request.text, request.context)
    
    # If DeepSeek fails, try DeepSeek Pro as fallback
    if not translations:
        translations = translate_with_deepseek_pro(request.text, request.context)
    
    if not translations:
        raise HTTPException(status_code=500, detail="Translation failed")
    
    return TranslationResponse(translations=translations)

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)