# Curio: The Anonymous Classroom

Curio is an AI-augmented classroom Q&A platform designed to remove the fear of judgment ("Log kya kahenge") by allowing students to ask questions anonymously. It features an AI agent that provides immediate answers to students while aggregating insights for teachers in real-time.

## 🚀 Features

- **Anonymous Participation:** Students join sessions via a 6-digit code without needing to login.
- **AI-Powered Answers:** An AI agent (Google Gemini 3.0 Flash) provides instant responses to student doubts.
- **Toxicity Guard:** All questions are screened for toxicity before being processed.
- **Live Teacher Dashboard:** Teachers can monitor class confusion trends and view questions in real-time.
- **Smart Grouping:** Similar questions are grouped together to help teachers focus on key topic areas.

## 🛠️ Tech Stack

### Frontend

- **Framework:** React 19 (via Vite)
- **Styling:** Tailwind CSS (v4)
- **UI Components:** Shadcn/UI (Radix Primitives)
- **State/Data Fetching:** TanStack Query

### Backend

- **Framework:** FastAPI (Python 3.13+)
- **Database:** SQLite (with SQLModel ORM)
- **AI Engine:** Google Gen AI SDK (Gemini 3.0 Flash)
- **Package Management:** uv

## 📋 Prerequisites

Ensure you have the following installed:

- **Python 3.13+**
- **Node.js 18+** & **npm**
- **uv** (Recommended Python package manager)

## 🏗️ Installation & Setup

### 1. Backend Setup

The backend handles the API, database, and AI processing.

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment and install dependencies using uv
uv sync

# Alternatively, using standard pip:
# python -m venv .venv
# source .venv/bin/activate  # On Windows: .venv\Scripts\activate
# pip install -e .

# Set up Environment Variables
# Copy the example environment file and add your Google API Key
cp .env.example .env
# Now edit .env and replace 'your_google_api_key_here' with your actual Gemini API key
```

To run the backend development server:

```bash
# Using uv
uv run uvicorn main:app --reload

# Or with standard python
# uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.
Explore the API documentation at `http://localhost:8000/docs`.

### 2. Frontend Setup

The frontend provides the user interface for both students and teachers.

```bash
# Navigate to the frontend directory
cd frontend

# Install dependencies
npm install

# Run the development server
npm run dev
```

The application will be accessible at `http://localhost:5173`.

## 📖 Usage Guide

### 👨‍🏫 For Teachers

**Goal:** Create a classroom session and monitor student questions.

1. **Start a Session:** Navigate to the **[Teacher Dashboard](http://localhost:5173/teacher)**.
   - _Link:_ `http://localhost:5173/teacher`
2. **Create:** Enter your **Teacher ID** (e.g., `teacher_001`) and the **Subject Name** (e.g., `Physics 101`).
3. **Share Code:** Click "Start Session". A unique **6-digit code** (e.g., `PHY-88`) will be generated. Share this code with your students.
4. **Monitor:** You will be redirected to the **Monitor Dashboard**. Watch questions appear in real-time, grouped by topic.

### 👩‍🎓 For Students

**Goal:** Join a session and ask questions anonymously.

1. **Join:** Go to the **[Home Page](http://localhost:5173)**.
   - _Link:_ `http://localhost:5173`
2. **Enter Code:** Type in the **6-digit Session Code** provided by your teacher (e.g., `PHY-88`).
3. **Ask:** Type your question in the text box.
4. **Learn:**
   - Receive an **immediate answer** from the AI agent.
   - See other students' questions (anonymously).

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.
