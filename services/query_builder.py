# query_buider.py ################################
from models.resume import ResumeProfile

def build_search_query(profile, location: str):
    # prefer role over skills
    if profile.roles:
        return profile.roles[0]

    if profile.skills:
         return f"{profile.skills[0]} developer"
    
    return f"{' '.join(profile.skills)} {profile.roles[0]} jobs in {location}"