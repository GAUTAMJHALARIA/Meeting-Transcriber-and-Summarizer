import google.generativeai as genai

genai.configure(api_key="AIzaSyCpBixDk37d92bP_gQxL2p1akhbiEX5nWA")
model = genai.GenerativeModel("gemini-1.5-pro-latest")

def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text

def generate_summary(transcript):
    return ask_gemini(f"Summarize the following meeting transcript in bullet points:\n{transcript}")

def extract_topics(transcript):
    return ask_gemini(f"List the key topics discussed in this meeting:\n{transcript}")

def extract_actions(transcript):
    return ask_gemini(f"List the action items from this meeting with responsible people if mentioned:\n{transcript}")

def highlight_decisions(transcript):
    return ask_gemini(f"Highlight important decisions made during this meeting:\n{transcript}")
