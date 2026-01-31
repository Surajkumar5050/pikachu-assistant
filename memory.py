import json
import os

MEMORY_FILE = "long_term_memory.json"

# --- SHORT TERM MEMORY (RAM) ---
short_term = {
    "last_app_opened": None,
    "last_browser_used": "default",
    "last_file_path": None,
    "last_action_type": None
}

# --- LONG TERM MEMORY (Hard Disk) ---
def load_long_term():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r') as f:
                return json.load(f)
        except:
            return {} 
    return {}

def save_long_term(key, value):
    data = load_long_term()
    data[key] = value
    with open(MEMORY_FILE, 'w') as f:
        json.dump(data, f, indent=4)

def update_context(action_type, target=None):
    short_term["last_action_type"] = action_type
    
    if action_type == "open_app":
        short_term["last_app_opened"] = target
    elif action_type == "open_url":
        short_term["last_browser_used"] = target
    elif action_type == "send_file" or action_type == "list_files":
        short_term["last_file_path"] = target

def get_context_string():
    """Returns a summary of BOTH Short-Term and Long-Term memory."""
    long_term_data = load_long_term() # Load your name/prefs
    
    return f"""
    [CURRENT CONTEXT STATE]
    - KNOWN USER INFO: {long_term_data}  <-- THIS WAS MISSING
    - Last App Opened: {short_term['last_app_opened']}
    - Last Browser Used: {short_term['last_browser_used']}
    - Last File/Folder: {short_term['last_file_path']}
    """