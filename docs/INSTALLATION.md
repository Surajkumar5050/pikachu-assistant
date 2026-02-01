# ⚙️ Installation Guide

This guide covers everything you need to get the **Pikachu Desktop Assistant** running on your Windows machine.

---

## ✅ Prerequisites

Before you start, ensure you have these three things installed:

### **1. Python 3.10** (Strictly required due to dependency compatibility)

- **Download**: [python.org](https://www.python.org/downloads/)
- **⚠️ CRITICAL**: During installation, check the box **"Add Python to PATH"**. If you miss this, nothing will work.

**Verification:**
```powershell
python --version
# Should show: Python 3.10.x
```

---

### **2. Ollama** (Local AI Engine)

- **Download**: [ollama.com](https://ollama.com)
- **Verify**: Open a terminal (cmd) and type:
  ```powershell
  ollama
  ```
  If you see help text, you're good to go.

---

### **3. Git** (Optional but recommended)

- **Download**: [git-scm.com](https://git-scm.com/)
- Used to clone the repository easily.

**Alternative**: You can download the project as a ZIP file from GitHub instead.

---

## 🚀 Option 1: Automated Installation (Recommended)

We've built a `setup.bat` script that handles the heavy lifting.

### **Step 1: Download the Code**

> ⚠️ **Important:** Replace `YOUR_USERNAME` with the repository owner's GitHub username.  
> Example (this project):
> ```powershell
> git clone https://github.com/YOUR_USERNAME/pikachu-assistant.git
> ```

**Option B - Manual Download:**
1. Download the ZIP from GitHub
2. Extract it to a folder (e.g., `C:\pikachu-assistant`)
3. Open that folder

---

### **Step 2: Run the Installer**

1. **Double-click `setup.bat`** in the project folder

2. **What it does:**
   - ✅ Checks for Python 3.11/3.10
   - ✅ Creates a secure virtual environment (`venv`)
   - ✅ Installs all libraries from `requirements.txt`
   - ✅ Automatically pulls the AI model (`qwen2.5-coder:7b`) if missing
   - ✅ Generates your `.env` config file

3. **Wait for completion** - The AI model download is ~4.7GB and may take 5-15 minutes depending on your connection

---

### **Step 3: Add Your Telegram Token**

1. The setup script will create a file named **`.env`**
2. Open it with Notepad
3. Find the line:
   ```ini
   TELEGRAM_TOKEN=your_actual_token_here
   ```
4. Replace `your_actual_token_here` with your actual bot token
5. Save and close

> **Don't have a token?** See the [Configuration Guide](CONFIGURATION.md) for step-by-step instructions on creating a Telegram bot.

---

### **Step 4: Configure Auto-Start on Windows Boot (Optional)**

To make Pikachu start automatically when your computer turns on:

1. **Create a Shortcut:**
   - Navigate to your project folder (e.g., `C:\pikachu-assistant`)
   - Right-click on `run_silent.vbs`
   - Select **Show more options** → **Create shortcut**
   - A file named `run_silent - Shortcut` will appear

2. **Open the Startup Folder:**
   - Press **Windows Key + R** to open the Run dialog
   - Type exactly: `shell:startup`
   - Press **Enter** - the Startup folder will open

3. **Move the Shortcut:**
   - Drag and drop the shortcut from Step 1 into the Startup folder
   - (Optional) Remove " - Shortcut" from the filename to make it cleaner

✅ **Done!** Pikachu will now start silently in the background every time you boot Windows.

---

### **Step 5: Start the Assistant**

**Double-click `start_pikachu.bat`** to launch.

You should see:
```
🟢 Ollama connection verified
🤖 Loading model: qwen2.5-coder:7b
👂 Listening for wake word...
```

---

## 🛠️ Option 2: Manual Installation

If you prefer to know exactly what's happening under the hood:

### **1. Set Up the AI Model**

Open your terminal and run:

```powershell
ollama pull qwen2.5-coder:7b
```

> **Note**: This downloads about **4.7GB** of data. Ensure you have a stable internet connection.

**Verification:**
```powershell
ollama list
# Should show: qwen2.5-coder:7b
```

---

### **2. Create the Python Environment**

Open terminal in the project folder:

```powershell
# Create virtual environment named 'venv'
python -m venv venv

# Activate it
venv\Scripts\activate
```

**Success indicator**: You should see `(venv)` appear at the start of your command prompt.

---

### **3. Install Dependencies**

```powershell
pip install -r requirements.txt
```

**Expected output**: You should see packages installing, including:
- `speech_recognition`
- `pyttsx3`
- `python-telegram-bot`
- `opencv-python`
- `psutil`
- `pyautogui`
- And more...

---

### **4. Create Configuration File**

1. Create a file named **`.env`** in the root folder
2. Add this content:

```ini
# Telegram Bot Configuration
TELEGRAM_TOKEN=your_actual_token_here

# AI Model Settings
MODEL_NAME=qwen2.5-coder:7b
OLLAMA_URL=http://localhost:11434

# Optional: Voice Settings
WAKE_WORDS=pikachu,hey you
VOICE_RATE=150
VOICE_VOLUME=1.0
```

3. Replace `your_actual_token_here` with your actual Telegram Bot Token

---

### **5. Run the Assistant**

```powershell
python main.py
```

**For Telegram mode:**
```powershell
python tele_agent.py
```

---

## 📦 What Gets Installed?

### **Python Packages** (from `requirements.txt`)

| Package | Purpose |
|---------|---------|
| `speech_recognition` | Voice input processing |
| `pyttsx3` | Text-to-speech output |
| `python-telegram-bot` | Telegram bot interface |
| `opencv-python` | Camera/webcam access |
| `psutil` | System monitoring (CPU, RAM, battery) |
| `pyautogui` | Keyboard/mouse automation |
| `python-dotenv` | Environment variable management |
| `Pillow` | Image processing |
| `requests` | HTTP requests to Ollama |

### **AI Model**

- **Name**: `qwen2.5-coder:7b`
- **Size**: ~4.7GB
- **Purpose**: Local language model for intent recognition
- **Location**: Managed by Ollama (typically in `C:\Users\USERNAME\.ollama\models`)

---

## 🔧 Post-Installation Setup

### **1. Configure Telegram Bot** (Optional but Recommended)

See the [Configuration Guide](CONFIGURATION.md) for detailed instructions.

**Quick steps:**
1. Message [@BotFather](https://t.me/BotFather) on Telegram
2. Send `/newbot`
3. Follow prompts to create your bot
4. Copy the token to `.env`

---

### **2. Test Voice Recognition**

1. Run `python main.py`
2. Say: **"Pikachu"** (wake word)
3. Listen for the acknowledgment beep
4. Say: **"What time is it?"**

If the assistant responds, voice mode is working! 🎉

---

### **3. Test Telegram Mode**

1. Run `python tele_agent.py`
2. Open Telegram and find your bot
3. Send: `/start`
4. Send: **"What time is it?"**

If the bot responds, Telegram mode is working! 🎉

---

## 🐛 Troubleshooting

### ❌ Error: **"Python is not recognized..."**

**Cause**: Python is installed but not added to your System PATH.

**Fix:**
1. Uninstall Python completely
2. Reinstall from [python.org](https://www.python.org/)
3. **CHECK THE BOX** at the bottom: _"Add Python 3.x to PATH"_
4. Complete installation
5. Restart your terminal

**Verification:**
```powershell
python --version
# Should work now
```

---

### ❌ Error: **"Ollama connection refused"**

**Cause**: The Ollama background service isn't running.

**Fix:**
1. Open the **Ollama app** from your Start Menu
2. You should see a small llama icon 🦙 in your taskbar tray (bottom-right)
3. If not visible, search for "Ollama" and launch it
4. Wait 10 seconds, then try again

**Verification:**
```powershell
ollama list
# Should show your models
```

---

### ❌ Error: **"ffmpeg not found"** or **"PyAudio error"**

**Cause**: `speech_recognition` needs system audio tools that aren't installed.

**Fix Option 1** (Recommended):
```powershell
pip install pipwin
pipwin install pyaudio
```

**Fix Option 2** (If above fails):
1. Download pre-compiled PyAudio wheel from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio)
2. Choose the correct version for Python 3.10 and your system (32-bit or 64-bit)
3. Install manually:
   ```powershell
   pip install PyAudio‑0.2.11‑cp310‑cp310‑win_amd64.whl
   ```

---

### ❌ Error: **"Bot doesn't reply on Telegram"**

**Cause**: Token misconfiguration or network issue.

**Checklist:**
1. ✅ Check your `.env` file - Did you save the token correctly?
   - Open `.env` with Notepad
   - Verify there are no extra spaces or quotes around the token
   - Format should be: `TELEGRAM_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

2. ✅ Restart the bot script:
   ```powershell
   # Stop with Ctrl+C
   python tele_agent.py
   ```

3. ✅ Check the console log:
   - If it says `Network Error` → Check your internet connection
   - If it says `Unauthorized` → Your token is invalid
   - If it says `Conflict` → Another instance of the bot is running (close it)

4. ✅ Test your token manually:
   ```powershell
   # Replace YOUR_TOKEN with your actual token
   curl https://api.telegram.org/botYOUR_TOKEN/getMe
   ```
   Should return bot info in JSON format.

---

### ❌ Error: **"ModuleNotFoundError: No module named 'X'"**

**Cause**: Virtual environment wasn't activated before installing dependencies.

**Fix:**
```powershell
# Navigate to project folder
cd C:\path\to\pikachu-assistant

# Activate venv
venv\Scripts\activate

# Reinstall everything
pip install -r requirements.txt
```

---

### ❌ Error: **"Model not found"** or **"qwen2.5-coder:7b not available"**

**Cause**: AI model wasn't downloaded successfully.

**Fix:**
```powershell
# Pull the model manually
ollama pull qwen2.5-coder:7b

# Verify it's there
ollama list
```

**If download keeps failing:**
- Check disk space (need ~5GB free)
- Try a different network connection
- Use a smaller model temporarily: `ollama pull qwen2.5-coder:3b`
  - Update `.env`: `MODEL_NAME=qwen2.5-coder:3b`

---

### ❌ Error: **"PermissionError: [WinError 5] Access is denied"**

**Cause**: Python doesn't have permission to write to the installation directory.

**Fix:**
1. Right-click on Command Prompt → **Run as Administrator**
2. Navigate to project folder
3. Re-run the setup:
   ```powershell
   setup.bat
   ```

---

### ❌ Microphone Not Working

**Cause**: Windows privacy settings or wrong audio device.

**Fix:**
1. **Check Windows Settings:**
   - Open Settings → Privacy → Microphone
   - Ensure "Allow apps to access your microphone" is ON

2. **Test microphone:**
   ```powershell
   # Run this test script
   python -c "import speech_recognition as sr; print(sr.Microphone.list_microphone_names())"
   ```
   Should list available microphones.

3. **If wrong device selected:**
   - Edit `listener.py`
   - Find: `mic = sr.Microphone()`
   - Change to: `mic = sr.Microphone(device_index=1)` (try 0, 1, 2...)

---

### 💡 General Debugging Tips

1. **Check logs**: Look at the terminal output when running the assistant
2. **Run in verbose mode**: Some scripts support a `--debug` flag
3. **Restart Ollama**: Sometimes the LLM service gets stuck
4. **Fresh install**: Delete `venv` folder and run `setup.bat` again
5. **Ask for help**: Open an issue on GitHub with:
   - Your error message
   - Python version (`python --version`)
   - OS version (Windows 10/11)
   - Steps to reproduce

---

## ✅ Verification Checklist

Before considering installation complete, verify:

- [ ] Python 3.10 is installed and in PATH
- [ ] Ollama is running (icon in taskbar)
- [ ] Model `qwen2.5-coder:7b` is downloaded
- [ ] Virtual environment is created
- [ ] All packages from `requirements.txt` are installed
- [ ] `.env` file exists with valid Telegram token
- [ ] `python main.py` runs without errors
- [ ] Wake word detection works (voice mode)
- [ ] Telegram bot responds to `/start` (telegram mode)

---

## 🎯 Next Steps

Once installation is complete:

1. 📖 Read the [Configuration Guide](CONFIGURATION.md) to customize settings
2. 📚 Check out the [User Guide](USER_GUIDE.md) to learn available commands
3. 🏗️ Review the [Architecture Documentation](ARCHITECTURE.md) if you want to extend functionality

---

## 🆘 Still Having Issues?

If you've tried everything and still can't get it working:

1. **Check existing issues**: [GitHub Issues](https://github.com/YOUR_USERNAME/pikachu-assistant/issues)
2. **Create a new issue**: Include:
   - Operating System version
   - Python version
   - Full error message
   - Steps you've already tried
3. **Join the community**: [Discord/Forum link if available]

---

**Installation should take 15-30 minutes depending on your internet speed. Most of that time is downloading the AI model.**

🎉 **Welcome to Pikachu Desktop Assistant!**
