import logging
import asyncio
import os
from dotenv import load_dotenv
from telegram import Update, constants
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from brain import process_command
from muscles import execute_command, capture_webcam
import memory

# --- CONFIGURATION ---
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

if not TOKEN:
    print("❌ Error: TELEGRAM_TOKEN not found in .env file.")
    exit()

ALLOWED_USERS = [] 

# --- GLOBAL STATE FOR CAMERA ---
CAMERA_ACTIVE = False

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# --- THE CAMERA LOOP TASK ---
async def camera_monitor_loop(bot, chat_id):
    """Sends a photo every 3 seconds while CAMERA_ACTIVE is True."""
    global CAMERA_ACTIVE
    
    status_msg = await bot.send_message(chat_id, "🔴 Live Feed Started (Updating every 3s)...")
    
    while CAMERA_ACTIVE:
        # 1. Take Photo
        photo_path = capture_webcam()
        
        # 2. Send it
        if photo_path and os.path.exists(photo_path):
            try:
                # We send a new photo because editing media is tricky in Telegram
                await bot.send_photo(chat_id, photo=open(photo_path, 'rb'))
            except Exception as e:
                print(f"Stream Error: {e}")
        
        # 3. Wait
        await asyncio.sleep(3) 

    await bot.send_message(chat_id, "xxxx Camera Feed Stopped.")

# --- MAIN HANDLER ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global CAMERA_ACTIVE
    user_text = update.message.text
    sender = update.message.from_user.username
    chat_id = update.effective_chat.id
    
    print(f"\n📩 Message from @{sender}: {user_text}")

    if ALLOWED_USERS and sender not in ALLOWED_USERS:
        await update.message.reply_text("⛔ Access Denied.")
        return

    # 1. Feedback
    await context.bot.send_chat_action(chat_id=chat_id, action=constants.ChatAction.TYPING)
    status_msg = await update.message.reply_text("⚡ Processing...")

    # 2. Send to Brain
    loop = asyncio.get_running_loop()
    try:
        command_json = await loop.run_in_executor(None, process_command, user_text)
    except Exception as e:
        await status_msg.edit_text(f"❌ Brain Error: {e}")
        return

    if command_json:
        action = command_json.get('action')
        
        # --- MEMORY UPDATE ---
        if action == "open_app":
            memory.update_context("open_app", target=command_json.get("app_name"))
        elif action == "open_url":
            memory.update_context("open_url", target=command_json.get("browser_path"))
        elif action in ["list_files", "send_file"]:
            memory.update_context("file_access", target=command_json.get("path"))
        elif action == "save_memory":
            key = command_json.get("key")
            val = command_json.get("value")
            memory.save_long_term(key, val)
            await status_msg.edit_text(f"🧠 Memory Updated: I'll remember that {key} is {val}.")
            return 

        if action == "general_chat":
            reply = command_json.get('response', "...")
            await status_msg.edit_text(f"💬 {reply}")

        # --- CAMERA STREAM TOGGLE ---
        elif action == "camera_stream":
            val = command_json.get("value")
            if val == "on":
                if not CAMERA_ACTIVE:
                    CAMERA_ACTIVE = True
                    await status_msg.edit_text("👀 Camera ON. Initializing feed...")
                    asyncio.create_task(camera_monitor_loop(context.bot, chat_id))
                else:
                    await status_msg.edit_text("⚠️ Camera is already running!")
            elif val == "off":
                CAMERA_ACTIVE = False
                await status_msg.edit_text("🛑 Stopping camera feed...")

        # --- SLEEP MODE ---
        elif action == "system_sleep":
            await status_msg.edit_text("💤 Putting laptop to sleep...")
            execute_command(command_json)

        # --- BATTERY CHECK ---
        elif action == "check_battery":
            await status_msg.edit_text("🔋 Checking power levels...")
            battery_status = execute_command(command_json)
            await update.message.reply_text(battery_status)

        # --- SYSTEM HEALTH CHECK (NEW) ---
        elif action == "check_health":
            await status_msg.edit_text("🏥 Performing system diagnostic...")
            health_report = execute_command(command_json)
            await update.message.reply_text(health_report)

        # --- SCREENSHOT ---
        elif action == "take_screenshot":
            await status_msg.edit_text("📸 Capture...")
            image_path = execute_command(command_json)
            if image_path:
                await status_msg.edit_text("📤 Uploading...")
                await update.message.reply_photo(photo=open(image_path, 'rb'))
            else:
                await status_msg.edit_text("❌ Screenshot failed.")

        # --- LIST FILES ---
        elif action == "list_files":
            raw_path = command_json.get('path')
            # Basic path resolution
            if "desktop" in raw_path.lower():
                raw_path = os.path.join(os.path.expanduser("~"), "Desktop")
            elif "downloads" in raw_path.lower():
                raw_path = os.path.join(os.path.expanduser("~"), "Downloads")
                
            await status_msg.edit_text(f"📂 Reading folder: {raw_path}...")
            
            if os.path.exists(raw_path) and os.path.isdir(raw_path):
                try:
                    files = os.listdir(raw_path)
                    if files:
                        files.sort()
                        files = files[:30] # Limit to 30
                        formatted_list = [f"🔹 {f}" for f in files]
                        file_list_text = "\n\n".join(formatted_list)
                        header = f"📂 **Contents of {os.path.basename(raw_path)}:**\n━━━━━━━━━━━━━━━━\n"
                        full_message = header + file_list_text
                        
                        if len(full_message) > 4000:
                            await update.message.reply_text(full_message[:4000] + "\n...(Truncated)")
                        else:
                            await update.message.reply_text(full_message)
                    else:
                        await update.message.reply_text("📂 The folder is empty.")
                except Exception as e:
                    await update.message.reply_text(f"❌ Error: {e}")
            else:
                await update.message.reply_text("❌ Folder not found.")

        # --- SEND FILE ---
        elif action == "send_file":
            raw_path = command_json.get('path')
            if raw_path.startswith("file:///"): raw_path = raw_path.replace("file:///", "")
            
            file_path = os.path.normpath(raw_path)
            
            await status_msg.edit_text(f"🔎 Fetching: {os.path.basename(file_path)}")
            if os.path.exists(file_path) and os.path.isfile(file_path):
                await update.message.reply_text("📤 Uploading...")
                try:
                    await update.message.reply_document(document=open(file_path, 'rb'))
                except Exception as e:
                    await update.message.reply_text(f"❌ Upload Failed: {e}")
            else:
                await update.message.reply_text("❌ File not found.")

        # --- PHYSICAL ACTIONS (Apps/URL/System) ---
        else:
            if action == "close_app":
                target = command_json.get('app_name', 'application')
                await status_msg.edit_text(f"💀 Killing {target}...")
            elif action == "open_url":
                target = command_json.get('url', 'website')
                await status_msg.edit_text(f"🌐 Opening {target}...")
            elif action == "system_control":
                await status_msg.edit_text(f"⚙️ Adjusting System...")
            elif action == "open_app":
                target = command_json.get('app_name')
                await status_msg.edit_text(f"🚀 Opening {target}...")
            
            try:
                execute_command(command_json)
                await update.message.reply_text("✅ Done.")
            except Exception as e:
                await update.message.reply_text(f"❌ Execution Failed: {e}")
            
    else:
        await status_msg.edit_text("❓ I didn't understand that.")

if __name__ == "__main__":
    print("🚀 TELEGRAM BOT STARTED...")
    try:
        application = ApplicationBuilder().token(TOKEN).build()
        msg_handler = MessageHandler(filters.TEXT | filters.COMMAND, handle_message) 
        application.add_handler(msg_handler)
        application.run_polling()
    except Exception as e:
        print(f"❌ Critical Error: {e}")