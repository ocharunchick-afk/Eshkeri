import os
import sys
import time
import shutil
import atexit
import tempfile
import subprocess
import warnings
from PyQt5.QtCore import QObject, pyqtSignal, QTimer

warnings.filterwarnings("ignore")

try:
    import psutil
except ImportError:
    psutil = None

try:
    from pypresence import Presence
except ImportError:
    Presence = None

class SpooferEngine(QObject):
    tick = pyqtSignal(int, int, float, str)
    quest_completed = pyqtSignal(str)
    status_changed = pyqtSignal(bool, str)
    discord_status = pyqtSignal(bool)

    def __init__(self, stub_exe_path=None):
        super().__init__()
        candidates = [
            stub_exe_path,
            os.path.join(getattr(sys, '_MEIPASS', ''), "dummy_stub.exe"),
            os.path.join(os.path.dirname(sys.executable), "dummy_stub.exe"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "dummy_stub.exe"),
        ]
        self.stub_exe_path = None
        for c in candidates:
            if c and os.path.exists(c):
                self.stub_exe_path = c
                break

        # Directory structure for simulated games (realistic runtime, no mention of spoofer)
        self.games_base_dir = os.path.join(tempfile.gettempdir(), "GameClient_Runtime")
        os.makedirs(self.games_base_dir, exist_ok=True)
        self._detectable_db = None

        self.active_game = None
        self.active_process = None
        self.active_process_path = None
        self.rpc = None

        self.is_running = False
        self.elapsed_seconds = 0
        self.target_seconds = 15 * 60

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self._on_tick)

        self.discord_check_timer = QTimer()
        self.discord_check_timer.setInterval(3000)
        self.discord_check_timer.timeout.connect(self.check_discord_running)
        self.discord_check_timer.start()

        atexit.register(self.stop)

    def check_discord_running(self):
        running = False
        if psutil:
            for p in psutil.process_iter(['name']):
                try:
                    name = (p.info['name'] or '').lower()
                    if 'discord' in name:
                        running = True
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
        self.discord_status.emit(running)
        return running

    def start(self, game_dict):
        """Starts process spoofing with a visible game window for Discord detection"""
        if self.is_running:
            self.stop()

        self.active_game = game_dict
        game_name = game_dict.get("name", "Unknown Game")
        process_name = game_dict.get("process", "Game.exe")
        if not process_name.lower().endswith(".exe"):
            process_name += ".exe"

        window_title = game_dict.get("window_title", game_name)
        duration_min = game_dict.get("duration_minutes", 15)
        self.target_seconds = max(60, int(duration_min * 60))
        self.elapsed_seconds = 0

        # Build realistic directory structure
        path_rel = game_dict.get("path_rel", "")
        if not path_rel:
            path_rel = os.path.join(game_name, process_name)

        # Normalize relative path separators
        parts = [p.strip() for p in path_rel.replace("/", "\\").split("\\") if p.strip()]
        target_exe = os.path.join(self.games_base_dir, *parts)
        os.makedirs(os.path.dirname(target_exe), exist_ok=True)

        try:
            if os.path.exists(self.stub_exe_path):
                shutil.copy2(self.stub_exe_path, target_exe)
                # Launch with visible window so Discord detects it via EnumWindows
                self.active_process = subprocess.Popen(
                    [target_exe, window_title],
                    cwd=os.path.dirname(target_exe)
                )
                self.active_process_path = target_exe
                print(f"[Spoofer] Spawned game window: {target_exe} with title '{window_title}'")
        except Exception as e:
            print(f"[Spoofer] Process start error: {e}")

        # Connect to Discord RPC if client_id is available (or auto-resolved)
        client_id = game_dict.get("client_id")
        if not client_id:
            client_id = self._resolve_client_id(game_name, process_name)
            if client_id:
                game_dict["client_id"] = client_id

        if client_id and Presence:
            try:
                self.rpc = Presence(str(client_id))
                self.rpc.connect()
                # 100% authentic in-game presence (In Game / Online)
                self.rpc.update(
                    state="In Game",
                    details="Playing Online",
                    start=int(time.time())
                )
                print(f"[Spoofer] Discord RPC activated for {game_name} (ID: {client_id})")
            except Exception as e:
                print(f"[Spoofer] Discord RPC connect warning: {e}")
                self.rpc = None

        self.is_running = True
        self.timer.start()
        self.status_changed.emit(True, game_name)
        self._on_tick()

    def stop(self):
        """Cleanly stops process, Discord RPC and cleans up"""
        if not self.is_running and not self.active_process and not self.rpc:
            return

        self.timer.stop()
        self.is_running = False

        if self.rpc:
            try:
                self.rpc.clear()
                self.rpc.close()
            except Exception:
                pass
            self.rpc = None

        if self.active_process:
            try:
                self.active_process.terminate()
                self.active_process.wait(timeout=1.5)
            except Exception:
                try:
                    self.active_process.kill()
                except Exception:
                    pass
            self.active_process = None

        # Note: keep or clean executable
        if self.active_process_path and os.path.exists(self.active_process_path):
            try:
                os.remove(self.active_process_path)
            except Exception:
                pass
            self.active_process_path = None

        game_name = self.active_game.get("name", "") if self.active_game else ""
        self.status_changed.emit(False, game_name)

    def _on_tick(self):
        if not self.is_running:
            return
        self.elapsed_seconds += 1
        pct = min(100.0, (self.elapsed_seconds / self.target_seconds) * 100.0)

        rem = max(0, self.target_seconds - self.elapsed_seconds)
        rem_m, rem_s = divmod(rem, 60)
        time_str = f"{rem_m:02d}:{rem_s:02d}"

        self.tick.emit(self.elapsed_seconds, self.target_seconds, pct, time_str)

        if self.elapsed_seconds >= self.target_seconds:
            game_name = self.active_game.get("name", "") if self.active_game else ""
            self.stop()
            self.quest_completed.emit(game_name)

    def _resolve_client_id(self, game_name, process_name):
        if self._detectable_db is None:
            self._detectable_db = []
            candidates = [
                os.path.join(getattr(sys, '_MEIPASS', ''), "discord_detectable.json"),
                os.path.join(os.path.dirname(sys.executable), "discord_detectable.json"),
                os.path.join(os.path.dirname(os.path.abspath(__file__)), "discord_detectable.json"),
            ]
            for c in candidates:
                if c and os.path.exists(c):
                    try:
                        import json
                        with open(c, "r", encoding="utf-8") as f:
                            self._detectable_db = json.load(f)
                        break
                    except Exception:
                        pass

        if not self._detectable_db:
            return None

        gn_low = game_name.lower().strip()
        proc_low = process_name.lower().strip()

        # 1. Exact match by name
        for g in self._detectable_db:
            if g.get("name", "").lower() == gn_low:
                return str(g.get("id"))

        # 2. Match by executable filename
        for g in self._detectable_db:
            for ex in g.get("executables", []):
                ex_name = ex.get("name", "").lower().replace("\\", "/").split("/")[-1]
                if ex_name == proc_low:
                    return str(g.get("id"))

        # 3. Substring match
        for g in self._detectable_db:
            if gn_low in g.get("name", "").lower() or g.get("name", "").lower() in gn_low:
                return str(g.get("id"))

        return None
