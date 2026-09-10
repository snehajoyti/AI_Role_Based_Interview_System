from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware 
from app.api.interview import router as interview_router
from app.api.resume import router as resume_router


app = FastAPI(
    title="AI-Powered Role-Based Candidate Screening System",
    description="AI/ML based technical interview system using RAG.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(interview_router)
app.include_router(resume_router)


@app.get("/")
def home():
    return {
        "message": "AI-Powered Role-Based Candidate Screening  System is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
