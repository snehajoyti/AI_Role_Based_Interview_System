from app.rag.role_retrieve import retrieve_for_role 
from app.services.llm_service import generate_response 



def generate_interview_question(
    role: str,
    resume_profile: dict,
    topic:str,
    top_k_per_book: int = 2
):
    # 1. Retrieve relevant knowledge from role-specific books
    retrieved_chunks = retrieve_for_role(
        role=role,
        query=topic,
        top_k_per_book=top_k_per_book 
    )

    retrieved_chunks = retrieved_chunks[:3]

    if not retrieved_chunks:
        raise ValueError("No relevant knowledge found for the selected role.")

    # 2. Build RAG context
    context_parts = []

    for i, chunk in enumerate(retrieved_chunks, start=1):
        context_parts.append(
            f"""
source {i}: {chunk['source']}
page: {chunk['page_number']}

{chunk['text']}
"""
        )

    context = "\n".join(context_parts)

    #  3. Create prompt for the LLM
    prompt = f"""
You are conducting a technical interview for the role of {role}.

Candidate Resume Profile:
{resume_profile}

Interview Topic:
{topic}

Use the following knowledge retrieved from the role-specific knwoledge base:

{context}

Generate exactly ONE technical interview question.

Return the question directly in the response.
Do not return reasoning, explanation, analysis, or any other text.


Requirements:
- The question must be relevant to the selected role.
- The question should be influenced by the candidate's resume profile.
- The question must be grounded in the retrieved knowledge.
- Avoid generic or unrelated questions.
- Prefer a conceptual or pratical question that can access the candidate's understanding.
-Do not provide the answer.
- Return only the interview question.
"""

    #4. Generate question using Groq
    question = generate_response(prompt)


    return {
        "question": question.strip(),
        "topic": topic,
        "role": role,
        "sources": [
            {
                "source": chunk["source"],
                "page_number": chunk["page_number"],
                "distance": chunk["distance"]
            }
            for chunk in retrieved_chunks 
        ]
    }

