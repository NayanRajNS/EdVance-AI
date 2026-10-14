# 🚀 EdVance AI — Dual Student & Teacher Ecosystem

**EdVance AI** is a full-stack EdTech platform combining a **B2C Student Hub (7 AI tools)** with a **B2B Teacher Command Center (4 educator workflows)**, powered by a hybrid **Groq LPU + Google Gemini 2.5 Flash** inference engine.

## ✨ Key Features
### 🎓 Student Hub
1. **Snap & Simplify (OCR & Translation):** Strips dense textbook jargon and translates concepts into 6 global languages (English, Malayalam, Hindi, Spanish, French, Arabic).
2. **Live Writing Vision Tutor:** Real-time webcam HUD and step-by-step calculation error verification.
3. **Universal Exam Generator & Board Archive:** Practice sets and marking schemes tailored for ISC, CBSE, IGCSE, and IB curriculums.
4. **Visual Concept Hub:** Interactive simulations for molecular bonding, tectonic plate subduction, and historical timelines.
5. **Socratic AI Homework Assistant:** Guides students with hints without spoiling final answers.
6. **In-Browser Peer Study Rooms:** Lightweight collaborative video & chat rooms.
7. **Kid & Teen Culture Radar:** Live AI-curated space science, animated film, and music updates.

### 👩‍🏫 Teacher Command Center
1. **AI Assignment Creator:** Instant homework, quizzes, and grading rubrics.
2. **Smart Notebook & Paper Corrector:** Automated handwriting transcription, rubric matching, and line-by-line feedback.
3. **Adaptive Differentiation Engine:** Rewrites core lesson plans for Visual, Analytical, and Remedial learners.
4. **Class Analytics & Heatmap Dashboard:** Visualizes class-wide conceptual weak spots in real time.

## 🛠️ Tech Stack & Local Setup
* **Frontend:** HTML5, Tailwind CSS, Lucide Icons, WebRTC MediaDevices API
* **Backend:** Python, Flask, `python-dotenv`, `groq`, `google-genai`

```bash
pip3 install flask flask-cors groq google-genai python-dotenv
PORT=5001 python3 server.py
