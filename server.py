import os
from flask import Flask, jsonify, render_template, request
from flask_cors import CORS
from groq import Groq
from google import genai
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder='.', template_folder='.')
CORS(app)

groq_key = os.environ.get("GROQ_API_KEY")
gemini_key = os.environ.get("GEMINI_API_KEY")

groq_client = Groq(api_key=groq_key) if groq_key else None
gemini_client = genai.Client(api_key=gemini_key) if gemini_key else None

# List of active 2026 Groq models in priority order
GROQ_MODELS = [
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b",
    "qwen/qwen3.8-27b"
]

def generate_hybrid_response(system_prompt, user_prompt, prefer="groq"):
    """Uses preferred AI engine with automatic model & provider fallback."""
    # 1. If Gemini is preferred and has a valid key, try it first
    if prefer == "gemini" and gemini_client:
        try:
            res = gemini_client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"{system_prompt}\n\nTask:\n{user_prompt}"
            )
            return res.text
        except Exception:
            pass  # Automatically fall back to Groq if Gemini key fails

    # 2. Try active Groq models
    if groq_client:
        for model_name in GROQ_MODELS:
            try:
                completion = groq_client.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.6,
                    max_tokens=1024,
                )
                return completion.choices[0].message.content
            except Exception:
                continue

        # 3. Ultimate fallback: dynamically query available models on your Groq key
        try:
            available = groq_client.models.list()
            for m in available.data:
                if "whisper" not in m.id.lower() and "guard" not in m.id.lower():
                    completion = groq_client.chat.completions.create(
                        model=m.id,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ],
                        temperature=0.6,
                        max_tokens=1024,
                    )
                    return completion.choices[0].message.content
        except Exception as e:
            raise RuntimeError(f"Groq API error: {str(e)}")

    # 4. Final fallback to Gemini
    if gemini_client:
        res = gemini_client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"{system_prompt}\n\nTask:\n{user_prompt}"
        )
        return res.text

    raise ValueError("No working API keys found in .env!")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json or {}
    msg = data.get('message', '')
    lang = data.get('language', 'English')
    try:
        sys_prompt = f"You are EdVance AI Homework Assistant. Respond in {lang}. Give step-by-step Socratic hints and guidance without blindly giving away the final answer."
        reply = generate_hybrid_response(sys_prompt, msg, prefer="groq")
        return jsonify({'reply': reply})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/ai-action', methods=['POST'])
def ai_action():
    data = request.json or {}
    feature = data.get('feature', '')
    text = data.get('text', '')
    lang = data.get('language', 'English')
    board = data.get('board', 'ISC')

    prompts = {
        'simplify': (
            f"You are Snap & Simplify OCR. Strip away academic jargon, explain the core concept simply, and translate into {lang}.",
            text, "gemini"
        ),
        'vision': (
            f"You are a Live Writing Vision Tutor. Check this student calculation/handwriting line for errors, alert them to any mistake, and show the corrected step in {lang}.",
            text, "gemini"
        ),
        'exam': (
            f"You are a Universal Exam Generator for {board}. Generate 3 high-yield board exam practice questions with step-by-step marking scheme solutions in {lang}.",
            f"Topic: {text}", "groq"
        ),
        'culture': (
            f"You are the Kid & Teen Culture Radar. Generate 3 exciting, safe-space updates in {lang}: 1) Space/Science news, 2) Upcoming animated movie prediction, 3) Major music drop.",
            "Give me today's live radar updates.", "groq"
        ),
        'assignment': (
            "You are an AI Assignment Creator for teachers. Generate a structured homework assignment, 3 quiz questions with answers, and a grading rubric.",
            f"Topic: {text}", "groq"
        ),
        'corrector': (
            "You are a Smart Notebook & Paper Corrector. Provide automated transcription verification, rubric matching out of 10 marks, and constructive line-by-line feedback.",
            text, "gemini"
        ),
        'differentiate': (
            "You are an Adaptive Differentiation Engine. Rewrite this lesson plan into 3 distinct variants: 1) Visual Learners, 2) Analytical Thinkers, and 3) Remedial Student Support.",
            text, "groq"
        )
    }

    if feature not in prompts:
        return jsonify({'error': 'Invalid feature requested'}), 400

    sys_prompt, user_prompt, engine = prompts[feature]
    try:
        result = generate_hybrid_response(sys_prompt, user_prompt, prefer=engine)
        return jsonify({'result': result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=True)