import ollama
import json
import os
from dotenv import load_dotenv
from memory import get_context_string

# Load environment variables
load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME", "qwen2.5-coder:7b")

# Base prompt (The fixed rules)
BASE_SYSTEM_PROMPT = """
You are Pikachu, a smart laptop assistant with memory.
Your ONLY output must be valid JSON.

COMMANDS:
1. Camera: {"action": "camera_stream", "value": "on/off"}
   (Triggers: turn on/off camera, live video, stop video)
   
2. Sleep:  {"action": "system_sleep"}
   (Triggers: sleep, go to sleep, /sleep)
   
3. Screenshot: {"action": "take_screenshot"}
   (Triggers: screenshot, capture screen, ss)

4. Apps:   {"action": "open_app" or "close_app", "app_name": "name"}
   (Triggers: open/close notepad, chrome, spotify)

5. URLs:   {"action": "open_url", "url": "https://site.com"}
   (Triggers: open youtube, google, website)

6. Files:  
   - Send: {"action": "send_file", "path": "path"} (Triggers: give me, send, upload)
   - List: {"action": "list_files", "path": "path"} (Triggers: show files, list directory)

7. Memory: {"action": "save_memory", "key": "preference_key", "value": "value"}
   (Triggers: "My name is X", "I prefer Chrome")

8. Battery: {"action": "check_battery"}
   (Triggers: battery percentage, check battery, power status)

9. Health: {"action": "check_health"}
   (Triggers: system health, cpu usage, ram check, how is the pc)

10. Chat:  {"action": "general_chat", "response": "text"}

*** CRITICAL RULE: CONTEXT AWARENESS ***
Use the [CURRENT CONTEXT STATE] below to resolve words like "it", "that", "the app", "the folder".
- If user says "Close it" and Last App Opened is "Chrome" -> Close Chrome.
- If user says "List files in it" and Last Folder is "Downloads" -> List Downloads.
"""

def process_command(user_input):
    print(f"⚡ Sending to Qwen: {user_input}")
    
    # 1. Get Dynamic Context from Memory (RAM & Long Term)
    current_context = get_context_string()
    
    # 2. Combine Static Rules + Dynamic Context
    full_prompt = BASE_SYSTEM_PROMPT + "\n" + current_context
    
    try:
        response = ollama.chat(
            model=MODEL_NAME, 
            messages=[
                {'role': 'system', 'content': full_prompt},
                {'role': 'user', 'content': user_input},
            ],
            keep_alive=0 
        )
        content = response['message']['content']
        
        # Clean Markdown if AI adds it
        if "```" in content:
            content = content.replace("```json", "").replace("```", "").strip()
        
        data = json.loads(content)
        
        # --- PARANOID OVERRIDES (Safety Net) ---
        lower = user_input.lower()
        
        # 1. Force Camera
        if "camera" in lower and "on" in lower: 
            data = {"action": "camera_stream", "value": "on"}
        elif "camera" in lower and "off" in lower: 
            data = {"action": "camera_stream", "value": "off"}
            
        # 2. Force Sleep/Screenshot/Battery
        elif "/sleep" in lower: 
            data = {"action": "system_sleep"}
        elif "/screenshot" in lower or "screenshot" in lower: 
            data = {"action": "take_screenshot"}
        elif "battery" in lower: 
            data = {"action": "check_battery"}
            
        # 3. Force Health Check
        elif any(x in lower for x in ["cpu", "ram", "system health", "lag", "pc status"]):
            data = {"action": "check_health"}

        # 4. Force Memory Save
        elif "my name is" in lower:
            name_part = user_input.split("is")[-1].strip()
            name_part = name_part.replace(".", "").replace("!", "")
            data = {"action": "save_memory", "key": "user_name", "value": name_part}

        # 5. Force File Send (Safety against "Open" confusion)
        send_keywords = ["give", "send", "upload", "fetch", "get"]
        # Add safety checks so we don't accidentally override "health" or "battery" commands
        safe_to_override = True
        for k in ["list", "camera", "battery", "cpu", "ram", "health"]:
            if k in lower:
                safe_to_override = False
                break
                
        if any(k in lower for k in send_keywords) and safe_to_override:
            found_path = data.get('path') or data.get('url') or data.get('app_name')
            if found_path:
                data = {"action": "send_file", "path": found_path}

        return data

    except Exception as e:
        print(f"Error: {e}")
        return {"action": "general_chat", "response": "I had a brain glitch."}