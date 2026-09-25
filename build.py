import os
import sys
import subprocess
import shutil

def build():
    cur_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(cur_dir)

    print("=== STARTING BUILD FOR ESHKERI.EXE ===")

    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--noconsole",
        "--onefile",
        "--name=Eshkeri",
        "--icon=app_icon.ico",
        "--add-data=icons;icons",
        "--add-data=dummy_stub.exe;.",
        "--add-data=games_db.json;.",
        "--add-data=discord_detectable.json;.",
        "--add-data=app_icon.png;.",
        "--add-data=app_icon.ico;.",
        "--hidden-import=PyQt5.QtMultimedia",
        "--hidden-import=PyQt5.QtMultimediaWidgets",
        "--hidden-import=game_icons",
        "--hidden-import=pypresence",
        "--clean",
        "main.py"
    ]

    print("Running:", " ".join(cmd))
    res = subprocess.run(cmd)

    if res.returncode == 0:
        dist_exe = os.path.join(cur_dir, "dist", "Eshkeri.exe")
        target_exe = os.path.join(cur_dir, "Eshkeri.exe")
        if os.path.exists(dist_exe):
            # Terminate any running Eshkeri.exe before copying
            try:
                subprocess.run(["taskkill", "/F", "/IM", "Eshkeri.exe"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception:
                pass
            import time
            time.sleep(1)
            shutil.copy2(dist_exe, target_exe)
            print(f"\n[SUCCESS] Compiled executable created at:\n{target_exe}\nSize: {os.path.getsize(target_exe) / (1024*1024):.2f} MB")
    else:
        print("[ERROR] Build failed with code:", res.returncode)

if __name__ == "__main__":
    build()
