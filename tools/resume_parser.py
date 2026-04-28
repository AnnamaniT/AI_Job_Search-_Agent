# resume_parser.py ################################
from langchain_community.document_loaders import PyPDFLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from models.resume import ResumeProfile
from dotenv import load_dotenv

from utils.filehash import get_file_hash

import json
import re
import os
from config import USE_LLM, MODEL_NAME, CACHE_RESUME


def extract_json(text: str):
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise ValueError("No JSON found in LLM response")
    return json.loads(match.group())


def parse_resume(file_path: str) -> ResumeProfile:
    file_hash = get_file_hash(file_path)
    cache_file = f"cache/resumes/{file_hash}.json"

    if CACHE_RESUME and os.path.exists(cache_file):
        print("Loading resume from cache...")
        with open(cache_file) as f:
            data = json.load(f)
        return ResumeProfile(**data)

    if not USE_LLM:
        print("LLM disabled, using mock resume")
        return ResumeProfile(
            name="Test User",
            skills=["Python", "FastAPI"],
            experience_years=2,
            roles=["Backend Developer"]
        )

    loader = PyPDFLoader(file_path)
    pages = loader.load()
    resume_text = "\n".join(page.page_content for page in pages)

    with open("prompts/resume_prompt.txt") as f:
        template = f.read()

    prompt = ChatPromptTemplate.from_template(template)

    load_dotenv()
    llm = ChatGroq(model=MODEL_NAME)

    response = llm.invoke(prompt.format_messages(text=resume_text))

    usage = response.response_metadata.get("token_usage", {})
    print("TOKEN USAGE:", usage)

    if not response.content:
        raise ValueError("LLM returned empty response")

    data = extract_json(response.content)
   

    if CACHE_RESUME:
        os.makedirs("cache/resumes", exist_ok=True)
        with open(cache_file, "w") as f:
            json.dump(data, f, indent=2)

    

    return ResumeProfile(**data)