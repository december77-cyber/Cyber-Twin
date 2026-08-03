from fastapi import FastAPI, HTTPException, Header, Request, Response
from pydantic import BaseModel
import ollama
# from fastapi.middleware.cors import CORSMiddleware

users_inputs = []

app = FastAPI()
# app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class CheckInput(BaseModel):
    text: str
    platform: str  

@app.middleware("http")
async def gather_data(request: Request, call_next):
    if request.method == "OPTIONS":
        response = Response(status_code=200)
        response.headers['Access-Control-Allow-Origin'] = 'chrome-extension://jlinonccpgnaeggknafjegnpnjpbickm'
        response.headers['Access-Control-Allow-Methods'] = '*'
        response.headers['Access-Control-Allow-Headers'] = "Cyber-Twin-Key, Content-Type"

        return response


    response = await(call_next(request))
    response.headers['Access-Control-Allow-Origin'] = 'chrome-extension://jlinonccpgnaeggknafjegnpnjpbickm'
    return response

@app.post("/analyze-post")
def analyze_post(data: CheckInput, cyber_twin_key= Header(alias="Cyber-Twin-Key")):
    if cyber_twin_key != 'skibidi':
        raise HTTPException(status_code=401, detail="Unauthorized access denied")

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

