import time
import ollama
import os
import psutil
import requests
from datetime import datetime
from zyron.features.browser_control import navigate, read_page, scan_page, click_element, create_tab, close_tab
from dotenv import load_dotenv

load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5-coder:7b")

RESEARCH_SYSTEM_PROMPT = """
You are Zyron's Information Synthesis module.
Your goal is to extract a clear, concise, and factual answer to the USER QUERY from the provided PAGE CONTENT.

RULES:
1. **Be Exact**: If the answer is in the text (even if buried), extract it. 
2. **Contextual Awareness**: Look for dates, numbers, names, and snippets in search results.
3. **Handle Failure**: If you genuinely cannot find the answer, summarize what IS there rather than just saying "I couldn't find it".
4. **Natural Tone**: Avoid robotic phrases like "The provided content mentions". Just say the answer.
5. **Conciseness**: Keep it to one or two short sentences unless the user asked for a detailed explanation.
6. **Date/Time Priority**: If the User Query is about the current date, time, or day, ALWAYS use the **CURRENT DATE (Ground Truth)** provided. Ignore any dates in the search results that contradict it.
"""

def is_firefox_running():
    """Checks if any firefox.exe process is active."""
    for proc in psutil.process_iter(['name']):
        try:
            if "firefox" in proc.info['name'].lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False

def clean_html(html):
    """Very basic HTML text extraction for requests fallback."""
    import re
    # Remove script and style elements
    text = re.sub(r'<(script|style).*?>.*?</\1>', '', html, flags=re.DOTALL)
    # Remove all other tags
    text = re.sub(r'<.*?>', ' ', text)
    # Consolidate whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text[:8000] # Limit to 8k chars for LLM

def perform_research(query):
    search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    content = ""
    tab_id = None

    # 1. Decide: Browser vs Headless
    if is_firefox_running():
        # Option A: Use Firefox Background Tab
        tab_id = create_tab(search_url, active=False)
        if tab_id:
            time.sleep(3) 
            result = read_page(tab_id=tab_id)
            if result and result.get("success"):
                content = result.get("content", "")
            close_tab(tab_id)
    
    # Fallback / Option B: Use Requests (Headless)
    if not content:
        try:
            headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
            response = requests.get(search_url, headers=headers, timeout=10)
            if response.status_code == 200:
                content = clean_html(response.text)
        except Exception as e:
            print(f"❌ Headless research failed: {e}")

    if not content:
        return "I tried both browser and network research but couldn't get any results. Are you offline?"

    # 2. Analyze with LLM
    now = datetime.now().strftime("%A, %B %d, %Y")
    prompt = f"CURRENT DATE (Ground Truth): {now}\nUSER QUERY: {query}\n\nPAGE CONTENT:\n{content}"
    
    try:
        response = ollama.chat(
            model=MODEL_NAME,
            messages=[
                {'role': 'system', 'content': RESEARCH_SYSTEM_PROMPT},
                {'role': 'user', 'content': prompt},
            ],
            keep_alive=0
        )
        return response['message']['content']
    except Exception as e:
        print(f"❌ Synthesis error: {e}")
        return "I found the info but had trouble processing it."

if __name__ == "__main__":
    print(perform_research("Who is CEO of OpenAI?"))
