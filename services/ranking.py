# ranking.py ################################
from models.resume import ResumeProfile
from models.job import Job
from tools.cache_fetch import get_cached_description
from utils.logger import debug

def score_job(job, profile):
    full_text = get_cached_description(job.url).lower()
    
    score = 0
    for skill in profile.skills:
        if skill.lower() in full_text:
            score += 1

    return score

def rank_jobs(jobs, profile):
    scored = []

    for job in jobs:
        s = score_job(job, profile)
        debug(f"{job.title} → score {s}")
        scored.append((job, s))

    scored.sort(key=lambda x: x[1], reverse=True)

    return [job for job, score in scored]   

def deduplicate_jobs(jobs):
    seen = set()
    unique = []

    for job in jobs:
        key = (job.title.lower(), job.company.lower())
        if key not in seen:
            seen.add(key)
            unique.append(job)

    return unique