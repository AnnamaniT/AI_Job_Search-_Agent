# AI Job Search Agent ########

An intelligent job search assistant built using LangChain and LLaMA 3.1 via Groq API. This application fetches real-time job listings and provides concise, meaningful summaries to help users quickly understand job roles.

# Features

- 🔍 Fetches real-time job listings using Adzuna API  
- 🤖 Uses LLM (LLaMA 3.1 via Groq) to summarize job descriptions  
- 📊 Displays structured and easy-to-read job insights  
- ⚡ Reduces time spent manually searching and reading job posts  

# Tech Stack

- Python  
- Streamlit  
- LangChain  
- Groq API (LLaMA 3.1)  
- Adzuna API  

# How It Works

1. User enters job role and location  
2. App fetches job listings using Adzuna API  
3. LLM processes and summarizes each job  
4. Results are displayed in a clean interface
   
# Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py

# Live Demo
https://job-search-agent-ai.streamlit.app/
