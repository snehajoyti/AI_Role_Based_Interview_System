# AI-Powered Role-Based Technical Interview System

## 1. Project Overview

The AI-Powered Role-Based Technical Interview System is an intelligent technical interview platform that generates personalized interview questions based on a candidate's resume, selected job role, and role-specific knowledge base.

The system uses Resume Processing, Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), FastAPI, React, FAISS, and SQLite to create a structured interview workflow.

The main goal is to simulate a technical interview where questions are dynamically generated instead of using a fixed set of predefined questions.

## 2. Problem Statement

Traditional technical interview systems often use predefined questions that do not consider the candidate's background or skills.

This project addresses this problem by dynamically generating questions using:

* Candidate resume
* Selected target role
* Role-specific technical knowledge
* Retrieved knowledge from provided books
* Candidate's projects, skills, and technical experience

This makes the interview more personalized and context-aware.

## 3. Key Features

* Resume PDF upload
* Resume text extraction
* Resume profile extraction
* Target role selection
* Role-specific knowledge retrieval
* Retrieval-Augmented Generation (RAG)
* Semantic search using embeddings
* FAISS vector database
* Personalized technical question generation
* Candidate answer submission
* Interview session management
* Persistent database storage
* Final interview summary generation
* Strengths, weaknesses, and recommendations
* Source traceability for generated questions
* React-based interactive frontend
* FastAPI backend APIs

## 4. Technology Stack

### Frontend

* React.js
* Vite
* JavaScript
* HTML
* CSS

### Backend

* Python
* FastAPI
* Uvicorn
* Pydantic

### AI / ML

* Large Language Models (LLMs)
* Groq API
* OpenAI GPT-OSS-20B
* Sentence Transformers
* all-MiniLM-L6-v2
* Embeddings
* Retrieval-Augmented Generation (RAG)
* FAISS

### Resume Processing

* PyMuPDF

### Database

* SQLite
* SQLAlchemy

### Development Tools

* Git
* GitHub
* VS Code
* Python Virtual Environment

## 5. Knowledge Base

The project uses the provided technical books as the primary RAG knowledge source.

The knowledge base contains seven resources:

### AI / Machine Learning

1. Machine Learning - Tom Mitchell
2. The Hundred-Page Machine Learning Book - Andriy Burkov
3. Machine Learning for Absolute Beginners

### Data Science / Applied Machine Learning

4. Introduction to Machine Learning with Python
5. Master Machine Learning Algorithms - Jason Brownlee

### Advanced / Theoretical Machine Learning

6. Pattern Recognition and Machine Learning - Christopher Bishop
7. Artificial Intelligence, Machine Learning and Deep Learning

The resources are organized according to their role/domain and indexed for semantic retrieval.

## 6. System Architecture

The system follows this high-level architecture:

Candidate
↓
React Frontend
↓
FastAPI Backend
↓
Resume Processing + Role Selection
↓
RAG Pipeline
↓
Knowledge Base → Chunking → Embeddings → FAISS Retrieval
↓
LLM Question Generation
↓
Interview Answer Storage
↓
Final Summary Generation
↓
SQLite Database

## 7. End-to-End Workflow

### Step 1: Candidate Resume Upload

The candidate uploads a resume in PDF format through the React frontend.

The backend receives the PDF and extracts its text using PyMuPDF.

### Step 2: Resume Profile Extraction

The extracted resume text is processed to identify relevant candidate information such as:

* Skills
* Technologies
* Projects
* Experience
* Education
* Domain exposure

This profile is later used to personalize the interview.

### Step 3: Role Selection

The candidate selects a target role.

Currently supported roles include:

* AI/ML Engineer
* Data Scientist

The selected role determines which knowledge sources are used during retrieval.

### Step 4: Knowledge Base Preparation

The provided PDF books are processed using:

PDF Documents
↓
Text Extraction
↓
Text Chunking
↓
Embeddings
↓
FAISS Vector Index

The documents are divided into smaller chunks with overlap to preserve contextual information.

The Sentence Transformer model `all-MiniLM-L6-v2` is used to generate embeddings.

The embeddings are stored in FAISS indexes for efficient semantic similarity search.

## 8. RAG Pipeline

The Retrieval-Augmented Generation pipeline is one of the core components of the system.

Candidate Resume + Selected Role + Interview Topic
↓
Semantic Query
↓
Role-Specific Knowledge Base
↓
FAISS Retrieval
↓
Relevant Knowledge Chunks
↓
LLM Prompt
↓
Personalized Interview Question

The system retrieves relevant knowledge from the selected role's knowledge base before generating the interview question.

This helps keep generated questions grounded in the provided technical resources.

## 9. Personalized Question Generation

Questions are not predefined.

The question generation process considers:

* Selected job role
* Candidate resume profile
* Interview topic
* Retrieved knowledge
* Source information

The LLM is instructed to generate one technical question that is:

* Relevant to the selected role
* Influenced by the candidate's resume
* Grounded in retrieved knowledge
* Conceptual or practical
* Suitable for technical interview evaluation

The generated question also stores its source information, including the source book and page number.

## 10. Interview Session

After the first question is generated, the candidate answers through the frontend.

The answer is sent to the backend and stored in the database.

The system then generates the next question based on the interview flow.

Each interview session has a unique session ID.

## 11. Database Design

SQLite is used for persistent storage.

The database contains the following main tables:

### InterviewSession

Stores:

* Session ID
* Selected role
* Resume text

### InterviewQA

Stores:

* Session ID
* Interview question
* Candidate answer

### InterviewReport

Stores:

* Session ID
* Interview summary
* Strengths
* Weaknesses
* Recommendations

This allows the complete interview lifecycle to be persisted.

## 12. Backend API Endpoints

### Resume Upload

`POST /resume/upload`

Uploads and processes the candidate's resume PDF.

### Start Interview

`POST /interview/start`

Creates a new interview session.

### Select Role

`POST /interview/select-role`

Stores the selected target role and candidate profile.

### Generate Question

`POST /interview/generate-question`

Retrieves relevant knowledge and generates a personalized technical interview question.

### Submit Answer

`POST /interview/answer`

Stores the candidate's answer for the current interview question.

### Generate Final Summary

`GET /interview/summary/{session_id}`

Generates the final interview assessment using the stored questions and candidate answers.

## 13. Final Interview Summary

After the interview, the system generates a structured final summary containing:

### SUMMARY

Overall assessment of the candidate.

### STRENGTHS

Strong technical areas demonstrated through the interview answers.

### WEAKNESSES

Areas where the candidate needs improvement.

### RECOMMENDATIONS

Practical suggestions for improving technical interview performance.

The final report is also persisted in the database.

## 14. Frontend Flow

The React frontend provides the following user flow:

1. Upload Resume
2. Select Target Role
3. Start Interview
4. Display Generated Question
5. Enter Candidate Answer
6. Submit Answer
7. Generate Next Question
8. Complete Interview
9. View Final Interview Summary

The interface communicates with the FastAPI backend using REST APIs.

## 15. Project Structure

```text
AI_Role_Based_Interview_System/
│
├── Backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── interview.py
│   │   │   └── resume.py
│   │   │
│   │   ├── rag/
│   │   │   ├── pdf_loader.py
│   │   │   ├── chunker.py
│   │   │   ├── vector_store.py
│   │   │   ├── retriever.py
│   │   │   └── role_retrieve.py
│   │   │
│   │   ├── services/
│   │   │   ├── llm_service.py
│   │   │   └── question_generator.py
│   │   │
│   │   ├── database.py
│   │   ├── models.py
│   │   ├── init_db.py
│   │   └── main.py
│   │
│   ├── knowledge_base/
│   │   ├── ai_ml/
│   │   ├── data_science/
│   │   └── advanced/
│   │
│   └── vector_store/
│       ├── ai_ml/
│       ├── data_science/
│       └── advanced/
│
├── Frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── main.jsx
│   │   └── index.css
│   ├── package.json
│   └── vite.config.js
│
├── PROJECT_DOCUMENT.md
└── README.md
```

## 16. RAG Implementation Details

The project uses:

* Chunk size: approximately 1000 characters
* Chunk overlap: approximately 200 characters
* Embedding model: `all-MiniLM-L6-v2`
* Embedding dimension: 384
* Vector search: FAISS `IndexFlatL2`

The system maintains separate vector indexes for different knowledge sources and retrieves relevant chunks based on the selected role and interview topic.

## 17. LLM Integration

The system uses the Groq API for LLM-based generation.

The configured model is:

`openai/gpt-oss-20b`

The API key is stored securely in an environment variable and is not hardcoded in the source code.

The LLM is used for:

* Technical question generation
* Final interview summary generation

## 18. Security and Configuration

Sensitive configuration such as the Groq API key is stored in a `.env` file.

The `.env` file is excluded from version control.

The project does not expose API credentials in the source code.

## 19. Error Handling

The backend includes validation and error handling for cases such as:

* Missing resume
* Invalid or empty resume content
* Unsupported interview role
* Missing knowledge retrieval results
* Missing interview session
* Missing interview answers
* Empty LLM responses

This helps maintain a reliable interview workflow.

## 20. Setup Instructions

### Backend

Navigate to the Backend directory:

```bash
cd Backend
```

Create and activate a Python virtual environment:

```bash
python -m venv venv
```

Activate the environment on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file and add:

```text
GROQ_API_KEY=your_api_key_here
```

Initialize the database:

```bash
python -m app.init_db
```

Start the backend:

```bash
uvicorn app.main:app --reload
```

Backend API:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend

Navigate to the Frontend directory:

```bash
cd Frontend
```

Install dependencies:

```bash
npm install
```

Start the development server:

```bash
npm run dev
```

Frontend:

```text
http://localhost:5173
```

## 21. Testing

The system was tested through the complete workflow:

* Resume upload
* Resume text extraction
* Resume profile extraction
* Role selection
* Knowledge retrieval
* Personalized question generation
* Candidate answer submission
* Multiple interview questions
* Final interview summary
* Database persistence

The complete end-to-end workflow was successfully tested using the React frontend and FastAPI backend.

## 22. Example Interview Flow

Candidate Resume
↓
AI/ML Engineer
↓
Resume Skills & Projects
↓
Relevant ML Knowledge Retrieval
↓
Personalized Technical Question
↓
Candidate Answer
↓
Next Interview Question
↓
Final Interview Summary

## 23. Future Improvements

Possible future improvements include:

* Adaptive difficulty based on candidate answers
* More supported job roles
* Better resume information extraction
* Hybrid keyword + semantic retrieval
* Improved source ranking
* Automated scoring of candidate answers
* Interview performance metrics
* Authentication and user accounts
* PostgreSQL support for production deployment
* Docker-based deployment
* Cloud deployment
* Speech-based interview interaction
* More advanced candidate analytics

## 24. Conclusion

The AI-Powered Role-Based Technical Interview System demonstrates how RAG and LLM technologies can be integrated with a modern backend and frontend architecture to create a personalized technical interview platform.

Instead of relying on predefined questions, the system dynamically retrieves relevant technical knowledge and generates questions based on the candidate's resume and selected role.

The project combines AI/ML, RAG, backend API development, database persistence, and frontend interaction into a complete end-to-end intelligent application.





