import time
from .core.voice import listen_for_command, take_user_input, speak
from .core.brain import process_command
from .agents.system import execute_command
from .utils.ui import print_header, print_status, print_command, print_zyron, print_error, Colors

# Import file tracker - it will auto-start when imported
import zyron.features.files.tracker as file_tracker

def main():
    print_header()
    print_status("✅", "Voice Engine Ready (Offline/Online)", Colors.GREEN)
    print_status("👁️", "Clipboard Monitor Active", Colors.GREEN)
    print_status("📁", "File Tracker Active", Colors.GREEN)
    print_status("👂", "Say 'Hey Pikachu' to start...", Colors.CYAN)
    
    while True:
        if listen_for_command():
            user_query = take_user_input()
            
            if user_query:
                print_command(user_query)
                
                # 1. Think
                print_status("🤔", "Analyzing intent...", Colors.YELLOW)
                action_json = process_command(user_query)
                
                if action_json:
                    # [QUIET MODE CHECK]
                    current_action = action_json[0].get("action")
                    if current_action == "web_research":
                        print_status("🔍", "Starting Quiet Research (Background Tab)...", Colors.BLUE)
                    else:
                        print_status("⚡", f"Executing: {current_action}", Colors.GREEN)
                    
                    # 2. Execute
                    response_text = execute_command(action_json)
                    
                    # 3. Respond
                    if response_text and isinstance(response_text, str) and not response_text.endswith(".png"):
                        print_zyron(response_text)
                        if response_text != "Done.":
                            speak(response_text)
                    else:
                        print_status("✅", "System action completed.", Colors.GREEN)
                else:
                    print_error("Failed to process command.")
                    speak("I'm sorry, my brain had a glitch.")
            
            time.sleep(1)
            print_status("👂", "Waiting for Pikachu...", Colors.CYAN)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}⚡ Zyron shutting down...{Colors.END}")
        
        # 1. Stop background tracking
        try:
            from .features.files import tracker as file_tracker
            file_tracker.stop_tracking()
        except: pass
        
        try:
            from .features import clipboard as clipboard_monitor
            clipboard_monitor.stop_monitoring()
        except: pass

        print(f"{Colors.GREEN}✅ Shutdown complete. Goodbye!{Colors.END}")