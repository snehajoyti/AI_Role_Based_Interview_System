from fastapi import APIRouter, UploadFile, File, HTTPException
from pypdf import PdfReader
from io import BytesIO
import re

router = APIRouter(
    prefix="/resume",
    tags=["Resume"]
)



def extract_section(text, section_name, next_sections):
    pattern = rf"{section_name}\s*(.*?)(?=\n(?:{'|'.join(next_sections)})|\Z)"

    match = re.search(
        pattern,
        text,
        re.IGNORECASE | re.DOTALL
    )

    if match:
        return match.group(1).strip()


    return ""



def extract_profile(resume_text):
    skills_match = re.search(
        r"TECHNICAL SKILLS\s*(.*?)(?=\nPROJECTS|\Z)",
        resume_text,
        re.IGNORECASE | re.DOTALL 
    )

    skills_text = (
        skills_match.group(1).strip() 
        if skills_match 
        else ""
    )

    return {
        "skills_and_technologies": skills_text,

        "projects": extract_section(
            resume_text,
            "PROJECTS",
            [
                "INTERNSHIP EXPERIENCE",
                "WORK EXPERIENCE",
                "CERTIFICATIONS"
            ]
        ),
        "experience": extract_section(
            resume_text,
            "INTERNSHIP EXPERIENCE",
            ["CERTIFICATIONS"]
        ),
        
        "education": extract_section(
            resume_text,
            "EDUCATION",
            ["TECHNICAL SKILLS", "PROJECTS"]
        )
    }


@router.post("/upload")
async def upload_resume(file:UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF resumes are supported."
        )

    file_content = await file.read()

    try:
        reader = PdfReader(BytesIO(file_content))

        resume_text = ""

        for page in reader.pages:
            text = page.extract_text()

            if text:
                resume_text += text + "\n"

            if not resume_text.strip():
                raise HTTPException(
                    status_code=400,
                    detail="Could not extract text from the PDF."
                )

            profile = extract_profile(resume_text)

            return {
                "message": "Resume processed successfully",
                "filename": file.filename,
                "text_length": len(resume_text),
                "profile": profile,
                "resume_text": resume_text.strip()
            }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Resume processing failed: {str(e)}"
        )





