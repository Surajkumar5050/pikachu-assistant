import json
import os
import time
from pathlib import Path

COMMAND_FILE_PATH = Path(os.environ.get('TEMP', '')) / 'zyron_firefox_commands.json'

def send_browser_command(action, **kwargs):
    """Writes a command to the shared JSON file for the native host to pick up."""
    # Ensure tabId is passed if provided
    command = {"action": action, **kwargs}
    
    try:
        commands = []
        if COMMAND_FILE_PATH.exists():
            try:
                with open(COMMAND_FILE_PATH, 'r') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        commands = data
            except: pass
            
        commands.append(command)
        
        with open(COMMAND_FILE_PATH, 'w') as f:
            json.dump(commands, f)
        
        # if the action expects a result (like "read" or "scan" or "create_tab"), wait for it
        if action in ["read", "scan", "create_tab", "click", "type", "scroll"]:
            return wait_for_result()
            
        return True
    except Exception as e:
        print(f"❌ Failed to queue browser command: {e}")
        return False

def wait_for_result(timeout=10):
    """Polls for the result file from the native host."""
    nav_path = Path(os.environ.get('TEMP', '')) / 'zyron_nav_result.json'
    
    # Clear old result first
    if nav_path.exists():
        try: os.remove(nav_path)
        except: pass
        
    start_time = time.time()
    while time.time() - start_time < timeout:
        if nav_path.exists():
            try:
                time.sleep(0.1)
                with open(nav_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    # Handle direct message or wrapped data
                    if not data: continue
                try: os.remove(nav_path)
                except: pass
                return data
            except:
                pass
        time.sleep(0.2)
        
    return {"success": False, "error": "Timeout waiting for browser response"}

def close_tab(tab_id):
    return send_browser_command("close_tab", tabId=tab_id)

def mute_tab(tab_id, mute=True):
    return send_browser_command("mute_tab", tabId=tab_id, value=mute)

def create_tab(url, active=True):
    """Returns the tabId of the created tab."""
    result = send_browser_command("create_tab", url=url, active=active)
    if isinstance(result, dict) and "tabId" in result:
        return result["tabId"]
    return None

def navigate(url, tab_id=None):
    if tab_id:
        return send_browser_command("navigate", url=url, tabId=tab_id)
    return send_browser_command("create_tab", url=url)

def click_element(selector, tab_id=None):
    if str(selector).isdigit():
        selector = f'[data-zyron-id="{selector}"]'
    return send_browser_command("click", selector=selector, tabId=tab_id)

def type_text(selector, text, tab_id=None):
    if str(selector).isdigit():
        selector = f'[data-zyron-id="{selector}"]'
    return send_browser_command("type", selector=selector, text=text, tabId=tab_id)

def scroll_page(direction="down", tab_id=None):
    return send_browser_command("scroll", direction=direction, tabId=tab_id)

def read_page(tab_id=None):
    return send_browser_command("read", tabId=tab_id)

def scan_page(tab_id=None):
    return send_browser_command("scan", tabId=tab_id)

