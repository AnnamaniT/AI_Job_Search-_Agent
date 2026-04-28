# job_search.py ################################
import requests
from models.job import Job
#from config import ADZUNA_APP_ID, ADZUNA_APP_KEY
from utils.logger import debug
import os
from dotenv import load_dotenv

BASE_URL = "https://api.adzuna.com/v1/api/jobs/in/search/1"
load_dotenv()
def search_jobs(query: str, location: str, results_per_page: int) -> list[Job]:
    params = {
        "app_id": os.getenv("ADZUNA_APP_ID"),
        "app_key": os.getenv("ADZUNA_APP_KEY"),
        "what": query,
        "where": location,
        "results_per_page": results_per_page
    }
    
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    debug(f"API URL: {response.url}")
    data = response.json()
    debug(f"API COUNT: { data.get("count")}")

    jobs = []

    for item in data.get("results", []):
        jobs.append(
            Job(
                title=item.get("title"),
                company=item.get("company", {}).get("display_name"),
                location=item.get("location", {}).get("display_name"),
                url=item.get("redirect_url"),
                description=item.get("description", "")
            )
        )

    return jobs