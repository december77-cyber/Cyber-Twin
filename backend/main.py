from fastapi import FastAPI, HTTPException, Header, Request, Response, Depends
from pydantic import BaseModel
import ollama
from sqlmodel import SQLModel, Session, create_engine, Field, select, or_
from sub_models import UserData, Location, Relations, Assets, Schedule

users_inputs = []

app = FastAPI()

class CheckInput(BaseModel):
    text: str
    platform: str

dataBaseURL = "sqlite:///./database.db"
engine = create_engine(dataBaseURL, connect_args={"check_same_thread": False}, echo=True)
SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session

def create_user_context(session: Session):
    whole_context_table = {'Location': [], 'Relations': [], 'Assets': [], 'Schedule': []}
    # statement = select(UserData.cyber_twin_response)
    statement1 = select(Location).where(Location.is_frequent_spot == True)
    statement2 = select(Relations).where(Relations.type.in_(["family", "friends", "dating", "work"]))
    statement3 = select(Assets).where(Assets.is_valuable == True)
    statement4 = select(Schedule).where(or_(Schedule.is_away_from_home == True, Schedule.is_important_event == True))

    for usr_object in session.exec(statement1):
        if 'Location' not in  whole_context_table:
            whole_context_table['Location'] = []

        whole_context_table['Location'].append(f"Name: {usr_object.name}, Granularity: {usr_object.granularity}, Is Frequent Spot: {usr_object.is_frequent_spot}")

    for usr_object in session.exec(statement2):
        if 'Relations' not in whole_context_table:
            whole_context_table['Relations'] = []

        whole_context_table['Relations'].append(f"Type: {usr_object.type}, Name: {usr_object.name}")

    for usr_object in session.exec(statement3):
        if 'Assets' not in whole_context_table:
            whole_context_table['Assets'] = []

        whole_context_table['Assets'].append(f"Name: {usr_object.name}, Is Valuable: {usr_object.is_valuable}")

    for usr_object in session.exec(statement4):
        if 'Schedule' not in whole_context_table:
            whole_context_table['Schedule'] = []

        whole_context_table['Schedule'].append(f"Time_frame: {usr_object.time_frame}, Time_category: {usr_object.time_category}, Is Away From Home: {usr_object.is_away_from_home}, Is Important Event: {usr_object.is_important_event}")

    print(f"Whole context table: {whole_context_table}")
    return whole_context_table
    

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
def analyze_post(data: CheckInput, cyber_twin_key= Header(alias="Cyber-Twin-Key"), session: Session = Depends(get_session)):
    if cyber_twin_key != 'skibidi':
        raise HTTPException(status_code=401, detail="Unauthorized access denied")

    users_inputs.append(data)
    print(f"Data gathered succesfully")
    print(f"Users text: {data.text}, platform: {data.platform}")


    user_context = create_user_context(session)

    print(f"User context created successfully: {user_context}")
    
    response = ollama.chat(
    model='llama3.1:8b',
    format=UserData.model_json_schema(),
    messages=[
        {   'role': 'system', 
            'content': "You are 'Cyber Twin', a deeply loyal, highly sophisticated personal cybersecurity and OPSEC (Operations Security) guardian. "
    "Your sole mission is to protect the user from exposing sensitive data, habits, location markers, PII, or answers to common security questions. "
    "Be candid, protective, concise, and analytical. Never lecture like an academic; give direct, sharp, and highly actionable feedback."
    "Take into account mainly the draft/ current users input but be also be aware of all other data prevously collected from the user."
    "Your mission is also to analyze user-generated text and extract all inadvertent leaks of personal data, routine patterns, and physical security vulnerabilities."
    """### EXTRACTION GUIDELINES:

    You are Cyber Twin, a personal OPSEC and cybersecurity guardian.

    Your mission is two-fold:
    0. RISK EVALUATION: Assess the OPSEC risk of the draft post. You must populate:
    - `risk_level`: Choose strictly between "LOW", "MEDIUM", or "HIGH".
    - `cyber_twin_response`: A direct, sharp 1-2 sentence explanation of the specific security or privacy hazard.
    - `suggested_fix`: A safe rewrite of the post or specific instructions on what details to omit.

    1. LOCATIONS:
    - Extract all geographic references, venues, landmarks, businesses, or home/office indicators.
    - Assign the appropriate granularity level based on how narrowly the location bounds the user's position.
    - Mark `is_frequent_spot=True` ONLY if the text explicitly indicates or strongly implies regular presence (e.g., references to "my gym", "commute", "neighborhood", "local spot", or "home").

    2. RELATIONS:
    - Extract the specific name, handle, or identifier of any mentioned person, pet, or acquaintance.
    - Categorize the relationship accurately based on explicit context. If ambiguous, use "other".
    - Pay special attention to pet names and family members, as these are common targets for security question recovery.

    3. ASSETS:
    - Extract mentions of high-value physical property (vehicles, luxury items, tech hardware) and critical digital assets (crypto wallets, specific security tools).
    - Mark `is_valuable=True` if loss, exposure, or theft of the item poses a significant physical, financial, or cybersecurity threat.

    4. SCHEDULE & TEMPORAL RISKS:
    - Extract any dates, durations, or timeframe references.
    - Classify the tense accurately into PAST, ONGOING, or FUTURE.
    - Mark `is_away_from_home=True` if the event implies the user's primary residence is or will be left unoccupied.
    - Mark `is_important_event=True` for high-stakes meetings, public appearances, or sensitive appointments.

    ### STRICT RULES:
    - Zero Hallucination: Extract ONLY details directly stated or logically required by the text. If a category has no mentions, leave its list empty.
    - Neutral Extraction: Do not summarize or editorialize within the entity fields; keep extracted names and timeframes concise and faithful to the source."""

        },
        {
            'role': 'user', 
            'content': f"""Analyze this social media draft intended for the platform: {data.platform}.
Identify any security, privacy, or personal safety risks (such as vacation plans indicating an empty house, location leaks, work projects 
disclosing intellectual property, family or pet names used in security questions). Your job is also Evaluating the risk (risk_level, cyber_twin_response, suggested_fix).
Extracting every identified entity into locations, relationships, assets, and schedule.

Draft to analyze: "{data.text}"
User data that you should take into account: are in here "{user_context}"
"""
        }
    ]
)
    
    ai_analysis = response['message']['content']
    ai_analysis = UserData.model_validate_json(ai_analysis)

    for location in ai_analysis.locations:
        session.add(location)
    for relation in ai_analysis.relationships:
        session.add(relation)
    for asset in ai_analysis.assets:
        session.add(asset)
    for schedule in ai_analysis.schedule:
        session.add(schedule)
    session.commit()

    print(f"AI analysis completed successfully: {ai_analysis}")

    return {
        "status": "success",
        "platform_analyzed": data.platform,
        "assessment": f"{ai_analysis.cyber_twin_response}\nRisk Level: {ai_analysis.risk_level}\nSuggested Fix: {ai_analysis.suggested_fix}", 
    }

