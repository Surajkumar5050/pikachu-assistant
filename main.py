import time
from listener import listen_for_command, take_user_input, speak
from brain import process_command
from muscles import execute_command

def main():
    print("⚡ SYSTEM ONLINE: Say 'Hey Pikachu' to start...")
    
    while True:
        # Step 1: Wait for the Wake Word ("Hey Pikachu")
        if listen_for_command():
            
            # Step 2: Listen for the specific instruction
            user_query = take_user_input()
            
            if user_query:
                # Step 3: Send to Brain (Get JSON)
                action_json = process_command(user_query)
                
                # Step 4: Execute with Muscles
                if action_json:
                    # Execute receives the text response now (e.g. "Moved file.")
                    response_text = execute_command(action_json)
                    
                    # Speak the result if it's text (ignore if it's an image path)
                    if response_text and isinstance(response_text, str) and not response_text.endswith(".png"):
                        speak(response_text)
                    else:
                        speak("Done.")
                else:
                    speak("I am not sure how to do that yet.")
            
            # Small pause to reset
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n⚡ System shutting down.")