from sqlalchemy import Column, Integer, String, Text 
from app.database import Base



class InterviewSession(Base):
    __tablename__= "interview_sessions"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True)
    role = Column(String)
    resume_text = Column(Text)



class InterviewQA(Base):
    __tablename__ = "interview_qa"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    question = Column(Text)
    answer = Column(Text)
    
class InterviewReport(Base):
    __tablename__ = "interview_reports"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    summary = Column(Text)
    strengths = Column(Text)
    weaknesses = Column(Text)
    recommendations = Column(Text)

