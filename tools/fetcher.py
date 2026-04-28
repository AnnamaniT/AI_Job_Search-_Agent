# fetcher.py ################################
import requests
from bs4 import BeautifulSoup
from utils.logger import debug

def fetch_full_description(url: str) -> str:
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Extract visible text from page
        text = soup.get_text(separator=" ", strip=True)

        return text

    except Exception as e:
        print(f"Failed to fetch {url}: {e}")
        return ""
    

