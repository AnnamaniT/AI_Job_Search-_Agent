# llm.py

from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def call_llm(prompt: str) -> str:
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
                 {
                "role": "system", 
                "content": "You explain job matches."
                },
                 {
                "role": "user",
                 "content": prompt
                 }
        ],
        temperature=0.3
    )

    return response.choices[0].message.content