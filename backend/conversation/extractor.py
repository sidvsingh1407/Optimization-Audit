import os
import json
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlocker
from backend.config.question_mapping import get_all_questions

# Use the environment variable for Gemini API
api_key = os.environ.get("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None


EXTRACTION_PROMPT = """
You are an expert AI extraction agent. Your goal is to map a user's conversational description of their AI usage into a strict JSON schema.

The schema includes standard multiple-choice questions and two text fields. Map the conversational intent to the most appropriate option letter ('a', 'b', 'c', 'd', 'e').

The multiple-choice questions are:
{questions}

Other fields:
- "monthly_spend": Choose from ["< $500", "$500-$2K", "$2K-$10K", "$10K+"] based on intent, or null if unknown.
- "tools_used": A comma-separated string of tools they mention, or null if none mentioned.

If the user has provided enough information to confidently guess an answer, provide the letter (e.g. "a").
If there is not enough information to guess, return null for that field.

Return ONLY a valid JSON object with the following structure, with NO markdown formatting, NO backticks:
{{
  "responses": {{
    "q1_1": "a",
    "q1_2": null,
    "q1_3": "c",
    ...
  }},
  "monthly_spend": "$500-$2K",
  "tools_used": "ChatGPT, GitHub Copilot"
}}

User Input Context:
{chat_history}
"""

def extract_structured_data(chat_history):
    """
    Calls Gemini to extract structured form data from the current chat history.
    """
    if not model:
        # Fallback if no API key
        return None

    questions_str = ""
    for q in get_all_questions():
        questions_str += f"- ID: {q['id']}\n  Label: {q['label']}\n  Options:\n"
        for opt in q['options']:
            questions_str += f"    {opt}\n"
        questions_str += "\n"

    chat_str = ""
    for msg in chat_history:
        chat_str += f"{msg['role'].upper()}: {msg['content']}\n"

    prompt = EXTRACTION_PROMPT.format(questions=questions_str, chat_history=chat_str)

    try:
        response = model.generate_content(
            prompt,
            safety_settings={
                HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlocker.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlocker.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlocker.BLOCK_NONE,
                HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlocker.BLOCK_NONE,
            }
        )

        # Clean JSON
        raw_text = response.text.strip()
        if raw_text.startswith("```json"):
            raw_text = raw_text[7:]
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3]

        return json.loads(raw_text.strip())

    except Exception as e:
        print(f"Extraction Error: {e}")
        return None
