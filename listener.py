import speech_recognition as sr
import pyttsx3

# Initialize
recognizer = sr.Recognizer()
engine = pyttsx3.init()
engine.setProperty('rate', 170)

# --- CONFIGURATION ---
# We accept variations because Google sometimes mishears "Pikachu"
WAKE_WORDS = ["pikachu", "pika", "peek a", "pick a", "picacho", "hey you"]

def speak(text):
    print(f"⚡ Pikachu: {text}")
    try:
        engine.say(text)
        engine.runAndWait()
    except:
        pass

def listen_for_command():
    with sr.Microphone() as source:
        print("\n👂 Listening for 'Hey Pikachu'...", end="", flush=True)
        
        # Fast adjustment to avoid blocking you
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        
        try:
            # Listen
            audio = recognizer.listen(source, timeout=4, phrase_time_limit=4)
            print(" Processing...", end="", flush=True)
            
            # Convert to text
            command = recognizer.recognize_google(audio).lower()
            
            # DEBUG: Print exactly what it heard
            print(f"\n   -> I heard: '{command}'")
            
            # Check if any wake word is in the command
            if any(word in command for word in WAKE_WORDS):
                speak("Pika Pika! I am listening.")
                return True
            else:
                return False
                
        except sr.WaitTimeoutError:
            return False
        except sr.UnknownValueError:
            # It heard sound but couldn't make words out of it
            return False
        except sr.RequestError:
            print("\n   -> Network Error")
            return False

def take_user_input():
    with sr.Microphone() as source:
        print("🎤 Command Mode: Speak now...")
        recognizer.adjust_for_ambient_noise(source, duration=0.2)
        try:
            audio = recognizer.listen(source, timeout=5)
            query = recognizer.recognize_google(audio).lower()
            print(f"   -> Command received: {query}")
            return query
        except Exception:
            print("   -> Didn't catch that.")
            return None

if __name__ == "__main__":
    while True:
        listen_for_command()