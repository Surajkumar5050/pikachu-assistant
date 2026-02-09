import zipfile
import os
from pathlib import Path

def package_extension():
    extension_dir = Path("firefox_extension")
    output_filename = "zyron_activity_monitor.zip"
    
    if not extension_dir.exists():
        print("❌ Error: firefox_extension folder not found!")
        return

    print(f"📦 Packaging extension from {extension_dir}...")
    
    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for file in extension_dir.glob("*"):
            if file.is_file():
                print(f"  + Adding {file.name}")
                zipf.write(file, arcname=file.name)
                
    print(f"\n✅ Created: {output_filename}")
    print("👉 Now upload this file to: https://addons.mozilla.org/developers/addon/submit/upload-listed")

if __name__ == "__main__":
    package_extension()
