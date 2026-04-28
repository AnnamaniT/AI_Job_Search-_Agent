# cache_fetch.py ################################
import json
import os
from .fetcher import fetch_full_description
from utils.logger import debug

CACHE_FILE = "cache/job_desc_cache.json"

def get_cached_description(url):
    # Ensure cache folder exists
    os.makedirs("cache", exist_ok=True)

    cache = {}

    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            cache = json.load(f)

    if url in cache:
        debug("Loaded description from cache")
        return cache[url]

    debug(f"Fetching from internet: {url}")
    text = fetch_full_description(url)

    cache[url] = text

    with open(CACHE_FILE, "w") as f:
        json.dump(cache, f)

    return text