from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse
import json
import os
import openai
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

UPLOAD_DIR = "admin_data"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/submit")
async def submit_data(data: dict = Body(...)):
    cv = data.get("cv")
    job_description = data.get("job_description")
    system_prompt = data.get("system_prompt")

    if cv:
        with open(os.path.join(UPLOAD_DIR, "cv.json"), "w") as cv_file:
            json.dump({"cv": cv}, cv_file, indent=4)

    if job_description:
        with open(os.path.join(UPLOAD_DIR, "jd.json"), "w") as jd_file:
            json.dump({"job_description": job_description}, jd_file, indent=4)

    if system_prompt:
        with open(os.path.join(UPLOAD_DIR, "prompt.json"), "w") as prompt_file:
            json.dump({"system_prompt": system_prompt}, prompt_file, indent=4)

    return JSONResponse(content={"message": "Data submitted successfully"})

@app.get("/get_scores")
async def get_scores():
    process_interviews()
    if os.path.exists("interview_results.json"):
        with open("interview_results.json", "r") as file:
            data = json.load(file)
        return JSONResponse(content={"data": data})
    else:
        return JSONResponse(content={"message": "No scores available"})
    
def load_json(file_path):
    with open(file_path, 'r') as file:
        return json.load(file)

def save_json(data, file_path):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=4)

def evaluate_response(response, job_description):
    prompt = f"""
    You are an experienced hiring manager tasked with evaluating a candidate's suitability for a position based on the following job description:

    {job_description}

    Below is the transcript of the interview with the candidate:

    {response}

    Please analyze the entire conversation and provide the following without any additional text:
    An overall rating of the candidate's performance on a scale from 1 to 10. Rating: integer only,
    A final verdict on whether the candidate is suitable for the role. Verdict: one or two lines only
    """
    openai.api_key = os.getenv("OPENAI_API_KEY")

    completion = openai.chat.completions.create(
        model="gpt-4",
        messages= [
            {"role": "system", "content": 'You are a helpful assistant.'},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100
    )
    evaluation = completion.choices[0].message.content
    print('Evaluation:', evaluation)
    return evaluation

def process_interviews():
    messages = load_json('conversation_data.json')
    job_description = load_json('admin_data/jd.json')['job_description']
    results = []
    for message in messages:
        candidate_id = message.get('candidate_id')
        response = message.get('response')
        if candidate_id and response:
            evaluation = evaluate_response(response, job_description)
            results.append({
                'CandidateId': candidate_id,
                'Evaluation': evaluation
            })
    save_json(results, 'interview_results.json')