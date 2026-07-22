from fastapi import FastAPI
from pydantic import BaseModel
import ollama

users_inputs = []

app = FastAPI()

class CheckInput(BaseModel):
    text: str
    platform: str  

@app.post("/analyze-post")
def analyze_post(data: CheckInput):
    users_inputs.append(data)
    print(f"Data gathered succesfully")
    print(f"Users text: {data.text}, platform: {data.platform}")
    
    response = ollama.chat(
    model='llama3.1:8b',
    messages=[
        {   'role': 'system', 
            'content': "You are 'Cyber Twin', a deeply loyal, highly sophisticated personal cybersecurity and OPSEC (Operations Security) guardian. "
    "Your sole mission is to protect the user from exposing sensitive data, habits, location markers, PII, or answers to common security questions. "
    "Be candid, protective, concise, and analytical. Never lecture like an academic; give direct, sharp, and highly actionable feedback."

        },
        {
            'role': 'user', 
            'content': f"""Analyze this social media draft intended for the platform: {data.platform}.
Identify any security, privacy, or personal safety risks (such as vacation plans indicating an empty house, location leaks, work projects disclosing intellectual property, family or pet names used in security questions).

Draft to analyze: "{data.text}"

You MUST format your response exactly using this Markdown layout:
### 🛡️ Cyber Twin Risk Assessment
**Risk Level:** [Low | Medium | High]

**Why:** [Briefly explain the security or privacy hazard in 1-2 sharp sentences]

**Suggested Fix:** [Provide an alternative way to write this post that hides the risk, or give advice on what to delete]
"""
        }
    ]
)
    
    ai_analysis = response['message']['content']

    return {
        "status": "success",
        "platform_analyzed": data.platform,
        "assessment": ai_analysis 
    }

