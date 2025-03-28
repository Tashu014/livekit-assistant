import gradio as gr
import requests
import json

API_URL = "http://127.0.0.1:8000"

def submit_data(cv, job_description, system_prompt):
    headers = {'Content-Type': 'application/json'}
    payload = {
        'cv': cv,
        'job_description': job_description,
        'system_prompt': system_prompt
    }
    response = requests.post(f"{API_URL}/submit/", data=json.dumps(payload), headers=headers)
    return response.json()

def fetch_scores():
    response = requests.get(f"{API_URL}/get_scores/")
    if response.status_code == 200:
        data = response.json().get('data', [])
        if isinstance(data, list) and data:
            # Just return the data rows, headers are defined in gr.Dataframe
            rows = []
            for entry in data:
                rows.append([
                    entry.get("CandidateId", ""),
                    entry.get("Evaluation", "")
                ])
            return rows
        else:
            return [["No scores available.", ""]]
    else:
        return [["Error retrieving scores.", ""]]

with gr.Blocks() as demo:
    with gr.Tabs():
        with gr.TabItem("Enter Interview Details"):
            with gr.Row():
                with gr.Column():
                    cv_input = gr.Textbox(label="CV", lines=10, placeholder="Enter CV text here...")
                    job_desc_input = gr.Textbox(label="Job Description", lines=10, placeholder="Enter Job Description here...")
                    prompt_input = gr.Textbox(label="System Prompt", lines=5, placeholder="Enter System Prompt here...")
                    submit_button = gr.Button("Submit")
                    output_text = gr.JSON(label="Response")
            submit_button.click(submit_data, inputs=[cv_input, job_desc_input, prompt_input], outputs=output_text)
        
        with gr.TabItem("View Scores"):
            scores_output = gr.Dataframe(headers=["CandidateId", "Evaluation"], interactive=False, wrap=True)
            refresh_button = gr.Button("Refresh Scores")
            refresh_button.click(fetch_scores, inputs=[], outputs=scores_output)

if __name__ == "__main__":
    demo.launch()
