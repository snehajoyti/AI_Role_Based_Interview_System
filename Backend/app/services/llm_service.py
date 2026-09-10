import os

from dotenv import load_dotenv 
from groq import Groq 


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__)
        )
    )
)

ENV_PATH = os.path.join(BASE_DIR, ".env")

load_dotenv(ENV_PATH)


GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in envirnoment variables")


client = Groq(api_key=GROQ_API_KEY)


MODEL_NAME = "openai/gpt-oss-20b"


def generate_response(prompt: str) -> str:
    response = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt 
            }
        ],
        max_tokens=1000,
        reasoning_effort="low"
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("LLM returned an empty response.")

    return content.strip()
