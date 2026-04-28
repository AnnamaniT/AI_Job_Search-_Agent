
# main.py ################################
from tools.resume_parser import parse_resume
from services.query_builder import build_search_query
from tools.job_search import search_jobs
from services.ranking import rank_jobs
from tools.explain import explain_top_jobs_batch
from config import MAX_RESULTS
from utils.logger import debug
from services.ranking import deduplicate_jobs
from utils.filehash import get_file_hash
import argparse


def run_pipeline(file_path: str, location: str):
    profile = parse_resume(file_path)
    query = build_search_query(profile, location)

    jobs = search_jobs(query, location, MAX_RESULTS)

    ranked = rank_jobs(jobs, profile)
    ranked = deduplicate_jobs(ranked)

    resume_hash = get_file_hash(file_path)

    explanations = explain_top_jobs_batch(
        ranked,
        profile,
        resume_hash
    )

    return ranked, explanations

