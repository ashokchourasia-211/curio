# **Product Requirement Document (Mini-PRD)**

Project Name: Curio (The Anonymous Classroom)

Version: 3.0 (API-Ready Build)

Date: December 14, 2025

Track: EdTech | Constraints: 6-Hour Hackathon

## **1\. Executive Summary**

**Curio** is an anonymous, AI-augmented classroom Q\&A platform. It removes the fear of judgment ("Log kya kahenge") by allowing students to ask doubts anonymously via a session code.

- **For Students:** A safe space where an AI Agent answers doubts instantly while they wait for the teacher.
- **For Teachers:** A real-time dashboard to see class confusion trends without needing to answer every single basic question manually.

## **2\. User Flows**

### **2.1 Teacher Flow (Admin)**

1. **Login:** Teacher authenticates (mocked for MVP).
2. **Create Session:** Enters Subject Name (e.g., "Physics 101") $\\rightarrow$ System returns a 6-digit code (e.g., PHY-88).
3. **Monitor:** Views a dashboard polling for new questions every 3 seconds.
4. **Control:** Can "End Session" to stop new questions.

### **2.2 Student Flow (Guest)**

1. **Join:** Enters Session Code PHY-88 on the landing page. No login required.
2. **Identity:** assigned a random session_user_id and display name (e.g., "Anonymous Panda").
3. **Ask:** Types/Speaks a doubt.
4. **Receive:**
   - **Immediate:** AI Agent response (if non-toxic).
   - **Blocked:** "Message flagged" error (if toxic).

## **3\. Functional Requirements**

| ID        | Feature                | Description                                                                                                | Priority |
| :-------- | :--------------------- | :--------------------------------------------------------------------------------------------------------- | :------- |
| **FR-01** | **Session Management** | Generate unique, collision-resistant 6-char codes.                                                         | P0       |
| **FR-02** | **Anonymous Posting**  | Students post messages linked _only_ to the Session Code.                                                  | P0       |
| **FR-03** | **AI Agent (Guard)**   | Single Agent using **Google ADK + Gemini 2.5 Flash**. Checks toxicity FIRST. If safe, generates an answer. | P0       |
| **FR-04** | **Polling Sync**       | Frontend polls /updates endpoint every 3s to fetch new messages.                                           | P0       |
| **FR-05** | **Teacher Auth**       | Simple Token/Basic Auth for creating sessions.                                                             | P1       |

## **4\. Technical Architecture**

- **Frontend:** React 19 + Tailwind CSS (Vite build).
- **Backend:** FastAPI (Python 3.11+).
- **Database:** SQLite (File-based for speed).
- **AI Engine:** Google Gen AI SDK (Agent Development Kit).
  - **Model:** gemini-2.5-flash (Optimized for <1s latency).
  - **Pattern:** Single-Shot Agent (System Prompt combines Toxicity Guard + Tutor Persona).

## **5\. Data Entities (Schema Draft)**

### **5.1 Session**

| Field      | Type      | Description                        |
| :--------- | :-------- | :--------------------------------- |
| id         | UUID      | Primary Key                        |
| code       | String(6) | Unique Entry Code (e.g., "PHY-88") |
| subject    | String    | Class Subject                      |
| teacher_id | String    | ID of creator                      |
| is_active  | Boolean   | true if accepting questions        |

### **5.2 Question (Doubt)**

| Field        | Type     | Description                              |
| :----------- | :------- | :--------------------------------------- |
| id           | UUID     | Primary Key                              |
| session_id   | UUID     | FK to Session                            |
| student_hash | String   | Anonymous ID (e.g., Browser Fingerprint) |
| student_name | String   | Display Name (e.g., "Anonymous Panda")   |
| text         | String   | The raw question                         |
| ai_response  | String   | The ADK generated answer                 |
| is_flagged   | Boolean  | True if Toxic                            |
| created_at   | DateTime | Timestamp                                |

## **6\. API Endpoint Requirements (Contract Basis)**

This section defines the inputs/outputs required for the OpenAPI generator.

### **A. Session Management**

- **POST /sessions**
  - **Input:** { "teacher_id": "str", "subject": "str" }
  - **Output:** { "session_id": "uuid", "code": "str" }
- **GET /sessions/verify/{code}**
  - **Input:** code (path param)
  - **Output:** { "valid": bool, "session_id": "uuid", "subject": "str" } OR 404 Not Found.

### **B. Q\&A Operations**

- **POST /questions**
  - **Input:** { "session_id": "uuid", "text": "str", "student_hash": "str" }
  - **Process:** Calls Google ADK Agent.
  - **Output:** { "question_id": "uuid", "ai_response": "str", "status": "posted" | "flagged" }
- **GET /questions/{session_id}** (Polling Endpoint)
  - **Input:** session_id (path param), last_seen_timestamp (query param, optional).
  - **Output:** List of Question objects posted _after_ the timestamp.
