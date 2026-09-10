from fastapi import APIRouter
from pydantic import BaseModel  

from app.database import SessionLocal
from app.models import InterviewQA, InterviewSession, InterviewReport 

from app.services.question_generator import generate_interview_question
from app.services.llm_service import generate_response


router = APIRouter(
    prefix="/interview",
    tags=["Interview"]
)


class InterviewRequest(BaseModel):
    role: str 
    resume_text: str


class RoleSelectionRequest(BaseModel):
    role: str
    resume_profile: dict 

class QuestionGenerationRequest(BaseModel):
    role: str
    resume_profile: dict
    topic:str 

class AnswerRequest(BaseModel):
    session_id: str
    question: str
    answer: str 


@router.post("/start")
def start_interview(request: InterviewRequest):
    db = SessionLocal() 

    session = InterviewSession(
        session_id=str(__import__("uuid").uuid4()),
        role=request.role,
        resume_text=request.resume_text
    )

    db.add(session)
    db.commit()
    db.refresh(session)

    db.close()

    return {
        "message": "Interview session started",
        "session_id": session.session_id,
        "role": request.role,
        "resume_received": bool(request.resume_text),
        "status": "ready"
    }


@router.post("/select-role")
def select_role(request: RoleSelectionRequest):

    return {
        "message": "Role selected successfully",
        "selected_role": request.role,
        "resume_profile": request.resume_profile,
        "status": "ready_for_rag"
    }

@router.post("/generate-question")
def generate_question(request: QuestionGenerationRequest):

    result = generate_interview_question(
        role=request.role,
        resume_profile=request.resume_profile,
        topic=request.topic 
    )

    return {
        "message": "Interview question generated successfully",
        "question": result["question"],
        "topic": result["topic"],
        "role": result["role"],
        "sources": result["sources"]
    }

@router.post("/answer")
def submit_answer(request: AnswerRequest):

    db = SessionLocal()

    try:
        qa = InterviewQA(
            session_id=request.session_id,
            question=request.question,
            answer=request.answer 
        )

        db.add(qa)
        db.commit()
        db.refresh(qa)

        return {
            "message": "Answer received successfully",
            "session_id": request.session_id,
            "question": request.question,
            "answer": request.answer,
            "status": "answer_saved",
            "qa_id": qa.id 
        }

    finally:
        db.close() 

@router.get("/summary/{session_id}")
def generate_interview_summary(session_id: str):
    db = SessionLocal()

    try: 
        session = db.query(InterviewSession).filter(
            InterviewSession.session_id == session_id 
        ).first()

        if not session:
            return {
                "message": "Interview session not found",
                "status": "error"
            }

        qa_records = db.query(InterviewQA).filter(
            InterviewQA.session_id == session_id 
        ).all()

        if not qa_records:
            return {
                "message": "No interview answers found",
                "status": "error"
            }
        qa_text = ""

        for i, qa in enumerate(qa_records, start=1):
            qa_text += f"""
    Question {i}:
    {qa.question}

    Candidate Answer:
    {qa.answer}

    """


        prompt = f"""
    You are evaluating a technical interview for the role of {session.role}.

    Below are the interview questions and candidate answers:

    {qa_text}

    Generate a concise structured interview summary.

    Include exactly these four sections:

    SUMMARY:
    Give an overall assessment of the candidate.

    STRENGTHS:
    Mention the Candidate's strongest technical areas based only on the answers.

    WEAKNESSES:
    Mention areas where the candidate needs improvement based only on the answers.

    RECOMMENDATIONS:
    Give pratical suggestions for improving technical interview performance.

    Do not invent information that is not present in the interview answers.
    """


        result = generate_response(prompt)

        report = InterviewReport(
            session_id=session_id,
            summary=result.strip(),
            strengths="Generated from interview responses",
            weaknesses="Generated from interview responses",
            recommendations="Generated from interview responses"
        )

        db.add(report)
        db.commit()
        db.refresh(report)

        return {
            "message": "Interview summary generated successfully",
            "session_id": session_id,
            "role": session.role,
            "summary": result.strip(),
            "status": "completed"
        }
        
    finally:
        db.close()


