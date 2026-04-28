# explain.py ################################
import os
import json
import hashlib

from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

from utils.logger import debug
from config import MODEL_NAME
from dataclasses import asdict

CACHE_DIR = "cache/explanations"


def build_explanation_key(job, resume_hash: str) -> str:
    text = f"{job.title}{job.company}{job.description}{resume_hash}"
    return hashlib.md5(text.encode()).hexdigest()


def format_explanation(raw):
    if raw is None:
        return "No explanation available."

    if isinstance(raw, list):
        formatted_exp = "\n".join(f"- {str(p).strip()}  " for p in raw if str(p).strip())       
        return formatted_exp
        
    # If string → force newlines before bullets
    text = str(raw)

    # Insert newline before every bullet except first
    text = text.replace(" •", "\n•")

    # Ensure it starts with bullet
    if not text.strip().startswith("•"):
        text = "• " + text.strip()

    #print(f"text: {text}")
    return text

def build_jobs_text(jobs):
    job_blocks = []

    for i, job in enumerate(jobs, 1):
        job_blocks.append(
            f"""
                Job {i}
                Title: {job.title}
                Company: {job.company}
                Location: {job.location}
                Description: {job.description[:500]}
                """
                        )

    return "\n".join(job_blocks)


def explain_top_jobs(jobs, profile, resume_hash: str):
    load_dotenv()
    llm = ChatGroq(model=MODEL_NAME)

    os.makedirs(CACHE_DIR, exist_ok=True)

    explanations = []

    for job in jobs:
        key = build_explanation_key(job, resume_hash)
        cache_file = os.path.join(CACHE_DIR, f"{key}.json")

        if os.path.exists(cache_file):
            print(f"Loading explanation from cache: {job.title}")
            with open(cache_file) as f:
                data = json.load(f)

            bullets = format_explanation(data.get("explanation", ""))
            explanations.append(bullets)
            continue

        debug(f"Explaining: {job.title} at {job.company}")

        with open("prompts/explain_prompt.txt") as f:
            template = f.read()

        prompt = ChatPromptTemplate.from_template(template)

        response = llm.invoke(
            prompt.format_messages(
                resume=asdict(profile),
                job=asdict(job)
            )
        )

        data = json.loads(response.content.strip())
        #print("RAW EXPLANATION TYPE:", type(data.get("explanation")))
        bullets = format_explanation(data.get("explanation", ""))
        explanations.append(bullets)

    return explanations

def explain_top_jobs_batch(jobs, profile, resume_hash: str):
    load_dotenv()
    llm = ChatGroq(model=MODEL_NAME)

    os.makedirs(CACHE_DIR, exist_ok=True)

    #  Build combined hash
    combined_text = "".join([job.title + job.company for job in jobs]) + resume_hash
    batch_hash = hashlib.md5(combined_text.encode()).hexdigest()

    cache_file = os.path.join(CACHE_DIR, f"batch_{batch_hash}.json")

    #  Check cache
    if os.path.exists(cache_file):
        print("Loading batch explanations from cache")
        with open(cache_file) as f:
            data = json.load(f)
    else:
        debug(f"Batch explaining {len(jobs)} jobs")

        with open("prompts/explain_prompt.txt") as f:
            template = f.read()

        prompt = ChatPromptTemplate.from_template(template)

        jobs_text = build_jobs_text(jobs)

        response = llm.invoke(
            prompt.format_messages(
                resume=asdict(profile),
                jobs=jobs_text
            )
        )

        raw = response.content.strip()
        debug(f"RAW LLM RESPONSE:\n, {raw}")  # 👈 keep this for debugging
        start = raw.find("{")
        end = raw.rfind("}") + 1
        json_str = raw[start:end]
        data = json.loads(json_str)

        with open(cache_file, "w") as f:
            json.dump(data, f, indent=2)

    # 👉 Convert to UI format
    explanations = []

    results = data.get("results", [])

    for item in results:
        bullets = format_explanation(item.get("explanation", []))
        explanations.append(bullets)

    return explanations