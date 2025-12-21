# Curio: The Anonymous Classroom

Curio is an AI-augmented classroom Q&A platform designed to remove the fear of judgment ("Log kya kahenge") by allowing students to ask questions anonymously. It features a sophisticated AI agent that provides immediate answers to students while aggregating insights for teachers in real-time.

## 🚀 Features

- **Anonymous Participation:** Students join sessions via a 6-digit code without needing to login.
- **AI-Powered Answers:** An AI agent powered by **Gemini 3-Flash-Preview** provides instant, thinking-capable responses to student doubts.
- **Smart Grouping:** Similar student questions are automatically grouped into threads using vector embeddings (**text-embedding-004**) to help teachers focus on key confusion areas.
- **Toxicity Guard:** All questions are screened for toxicity before being processed by the AI.
- **Live Teacher Dashboard:** Teachers can monitor class trends, view grouped questions, and provide a single answer to multiple similar queries.

## 🛠️ Tech Stack

### Frontend

- **Framework:** React 19 (Vite)
- **Styling:** Tailwind CSS v4 (with `tw-animate-css`)
- **UI Components:** Radix UI Primitives & Shadcn/UI (adapted for CSS-only v4)
- **State Management:** TanStack Query (React Query) v5
- **Routing:** React Router v7

### Backend

- **Framework:** FastAPI (Python 3.13+)
- **Database:** SQLite with **SQLModel** (SQLAlchemy + Pydantic)
- **AI Engine:** Google Gen AI SDK & **Google Agent Development Kit (ADK)**
- **Models:**
  - **Gemini 3-Flash-Preview** (Chat & Reasoning)
  - **text-embedding-004** (Vector Embeddings for Similarity)
- **Package Management:** `uv` (Fastest Python package manager)

## 📋 Prerequisites

Ensure you have the following installed:

- **Python 3.13+**
- **Node.js 20+** & **npm**
- **uv** (Recommended Python package manager) - [Install uv](https://github.com/astral-sh/uv)

## 🏗️ Installation & Setup

### 1. Backend Setup

The backend handles the API, database, AI processing, and vector grouping.

```bash
# Navigate to the backend directory
cd backend

# Create a virtual environment and install dependencies using uv
uv sync

# Set up Environment Variables
# Copy the example environment file and add your Google API Key
cp .env.example .env
# Edit .env and add your GOOGLE_API_KEY
```

To run the backend server:

```bash
uv run uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`.
Docs: `http://localhost:8000/docs`

### 2. Frontend Setup

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

1. **Start a Session:** Go to `/teacher`, enter your ID and Subject.
2. **Monitor:** Share the code (e.g., `MATH-12`) with students.
3. **Manage:** Watch groups of questions appear. Answer a group once to reply to all similar students.

### 👩‍🎓 For Students

1. **Join:** Enter the session code on the home page.
2. **Ask:** Post your question anonymously.
3. **Learn:** Get instant AI feedback and see what others are asking.

## 🤝 Contributing

1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/AmazingFeature`).
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
4. Push to the branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

Built with ❤️ by Antigravity for Advanced Agentic Coding.
