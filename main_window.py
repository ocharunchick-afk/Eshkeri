import os
import sys
import glob
import json
import random
from PyQt5.QtCore import (
    Qt, QPoint, QSize, pyqtSignal, QTimer, QUrl, QRect, QRectF, QSizeF, QThread
)
from PyQt5.QtGui import (
    QIcon, QPixmap, QFont, QColor, QPainter, QLinearGradient, QRadialGradient,
    QPainterPath, QPen, QCursor, QBrush, QPolygonF
)
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QScrollArea, QFrame, QDialog,
    QMessageBox, QSlider, QComboBox, QFileDialog,
    QGraphicsView, QGraphicsScene, QGraphicsProxyWidget,
    QGraphicsPixmapItem, QListWidget, QListWidgetItem
)
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem

from game_icons import create_cyber_game_icon

CYBER_YELLOW = "#FCEE0A"
CYBER_CYAN   = "#00F0FF"
CYBER_RED    = "#FF003C"
CYBER_GREEN  = "#00FF66"
CYBER_MAGENTA= "#D070FF"

class CyberGlitchButton(QPushButton):
    """Button with Cyberpunk hover glitch effects"""
    def __init__(self, text="", parent=None, is_yellow=False, is_red=False):
        super().__init__(text, parent)
        self.is_yellow = is_yellow
        self.is_red = is_red
        self.original_text = text
        self.glitch_timer = QTimer(self)
        self.glitch_timer.setInterval(40)
        self.glitch_timer.timeout.connect(self._glitch_tick)
        self.glitch_frames = 0
        self.setCursor(Qt.PointingHandCursor)
        self._update_stylesheet()

    def _update_stylesheet(self, glitch_border=False):
        if self.is_yellow:
            bg = CYBER_YELLOW if not glitch_border else "#FFF870"
            border = "#FFFFFF" if glitch_border else CYBER_YELLOW
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg};
                    border: 2px solid {border};
                    color: #000000;
                    font-family: 'Segoe UI', Consolas, sans-serif;
                    font-weight: bold;
                    font-size: 13px;
                    padding: 8px 16px;
                    border-radius: 2px;
                }}
                QPushButton:hover {{
                    background-color: #FFFFFF;
                    color: #000000;
                    border: 2px solid {CYBER_CYAN};
                }}
            """)
        elif self.is_red:
            bg = "rgba(56, 12, 20, 200)" if not glitch_border else "rgba(107, 20, 37, 220)"
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {bg};
                    border: 1px solid {CYBER_RED};
                    color: {CYBER_RED};
                    font-family: 'Segoe UI', Consolas, sans-serif;
                    font-weight: bold;
                    font-size: 13px;
                    padding: 8px 16px;
                    border-radius: 2px;
                }}
                QPushButton:hover {{
                    background-color: {CYBER_RED};
                    color: #FFFFFF;
                }}
            """)
        else:
            border = CYBER_YELLOW if glitch_border else CYBER_CYAN
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(16, 22, 34, 180);
                    border: 1px solid {border};
                    color: {CYBER_CYAN};
                    font-family: 'Segoe UI', Consolas, sans-serif;
                    font-weight: bold;
                    font-size: 13px;
                    padding: 8px 16px;
                    border-radius: 2px;
                }}
                QPushButton:hover {{
                    background-color: {CYBER_CYAN};
                    color: #000000;
                    border: 1px solid #FFFFFF;
                }}
            """)

    def enterEvent(self, event):
        self.glitch_frames = 4
        self.glitch_timer.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.glitch_timer.stop()
        self.setText(self.original_text)
        self._update_stylesheet(False)
        super().leaveEvent(event)

    def _glitch_tick(self):
        self.glitch_frames -= 1
        if self.glitch_frames > 0:
            glitch_chars = "!<>-_\\/[]{}—=+*^?#________"
            if len(self.original_text) > 2:
                idx = random.randint(0, len(self.original_text) - 1)
                scrambled = list(self.original_text)
                scrambled[idx] = random.choice(glitch_chars)
                self.setText("".join(scrambled))
            self._update_stylesheet(True)
        else:
            self.glitch_timer.stop()
            self.setText(self.original_text)
            self._update_stylesheet(False)


class GameCard(QFrame):
    start_requested = pyqtSignal(dict)
    delete_requested = pyqtSignal(str)

    def __init__(self, game_dict, is_active=False, get_opacity_fn=None, parent=None):
        super().__init__(parent)
        self.game_dict = game_dict
        self.is_active = is_active
        self.is_hovered = False
        self.get_opacity_fn = get_opacity_fn
        self.init_ui()

    def init_ui(self):
        self.setFixedHeight(120)
        self.update_style()

        layout = QHBoxLayout(self)
        layout.setContentsMargins(14, 10, 16, 10)
        layout.setSpacing(14)

        # Original Game Icon Badge
        self.lbl_icon = QLabel()
        self.lbl_icon.setFixedSize(68, 68)
        pix = create_cyber_game_icon(self.game_dict.get("id", ""), size=64)
        self.lbl_icon.setPixmap(pix)
        layout.addWidget(self.lbl_icon)

        # Info Box
        info_layout = QVBoxLayout()
        info_layout.setSpacing(3)

        self.title = QLabel(self.game_dict.get("name", "Unknown Game"))
        self.title.setFont(QFont("Impact", 14))
        self.title.setStyleSheet(f"color: {CYBER_YELLOW}; letter-spacing: 1px;")
        info_layout.addWidget(self.title)

        tags_layout = QHBoxLayout()
        tags_layout.setSpacing(8)

        proc_lbl = QLabel(f"⚙ {self.game_dict.get('process', '')}")
        proc_lbl.setFont(QFont("Consolas", 10))
        proc_lbl.setStyleSheet("color: #00F0FF; background: rgba(0, 240, 255, 30); border: 1px solid rgba(0,240,255,80); padding: 2px 6px; border-radius: 2px;")
        tags_layout.addWidget(proc_lbl)

        dur_lbl = QLabel(f"⏱ {self.game_dict.get('duration_minutes', 15)} MIN")
        dur_lbl.setFont(QFont("Consolas", 10, QFont.Bold))
        dur_lbl.setStyleSheet(f"color: {CYBER_YELLOW}; background: rgba(252, 238, 10, 30); border: 1px solid rgba(252,238,10,80); padding: 2px 6px; border-radius: 2px;")
        tags_layout.addWidget(dur_lbl)

        cat_lbl = QLabel(self.game_dict.get("category", "Quest"))
        cat_lbl.setFont(QFont("Segoe UI", 9))
        cat_lbl.setStyleSheet("color: #A0AEC0;")
        tags_layout.addWidget(cat_lbl)
        tags_layout.addStretch()

        info_layout.addLayout(tags_layout)

        desc = QLabel(self.game_dict.get("description", "Discord Quest for Orbs"))
        desc.setStyleSheet("color: #CBD5E1; font-size: 11px;")
        info_layout.addWidget(desc)

        layout.addLayout(info_layout, stretch=1)

        # Action Button
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(6)

        if self.is_active:
            self.btn_action = CyberGlitchButton("● СИМУЛЯЦИЯ...", is_yellow=True)
            self.btn_action.setEnabled(False)
        else:
            self.btn_action = CyberGlitchButton("▶ ЗАПУСК")
            self.btn_action.clicked.connect(lambda: self.start_requested.emit(self.game_dict))

        btn_layout.addWidget(self.btn_action)

        if self.game_dict.get("id", "").startswith("custom_"):
            btn_del = QPushButton("✖")
            btn_del.setFixedWidth(28)
            btn_del.setStyleSheet(f"color: {CYBER_RED}; border: none; background: transparent; font-size: 14px;")
            btn_del.setToolTip("Удалить игру")
            btn_del.clicked.connect(lambda: self.delete_requested.emit(self.game_dict["id"]))
            btn_layout.addWidget(btn_del, alignment=Qt.AlignRight)

        layout.addLayout(btn_layout)

    def set_active(self, active):
        self.is_active = active
        self.update_style()
        if active:
            self.btn_action.setText("● СИМУЛЯЦИЯ...")
            self.btn_action.is_yellow = True
            self.btn_action._update_stylesheet()
            self.btn_action.setEnabled(False)
        else:
            self.btn_action.setText("▶ ЗАПУСК")
            self.btn_action.is_yellow = False
            self.btn_action._update_stylesheet()
            self.btn_action.setEnabled(True)

    def enterEvent(self, event):
        self.is_hovered = True
        self.update_style()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self.is_hovered = False
        self.update_style()
        super().leaveEvent(event)

    def update_style(self):
        op = self.get_opacity_fn() if self.get_opacity_fn else 0.75
        alpha = int(op * 255)

        if self.is_active:
            border = CYBER_YELLOW
            bg = f"rgba(25, 38, 55, {min(255, alpha + 30)})"
        elif self.is_hovered:
            border = CYBER_CYAN
            bg = f"rgba(20, 30, 48, {min(255, alpha + 20)})"
        else:
            border = "rgba(0, 240, 255, 120)"
            bg = f"rgba(14, 18, 28, {alpha})"

        self.setStyleSheet(f"""
            GameCard {{
                background-color: {bg};
                border: 1px solid {border};
                border-radius: 4px;
            }}
        """)


class SandevistanOverlay(QWidget):
    """Transparent overlay on top of MainWindow to draw animated Sandevistan ghost trails and chromatic blur"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.is_active = False
        self.trail_points = []

    def paintEvent(self, event):
        if not self.is_active or len(self.trail_points) < 2:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        w, h = self.width(), self.height()

        # 1. Subtle Sandevistan temporal glow / chromatic scan overlay
        glow = QRadialGradient(w / 2, h / 2, max(w, h) / 1.5)
        glow.setColorAt(0.0, QColor(0, 255, 102, 18))
        glow.setColorAt(0.7, QColor(0, 240, 255, 12))
        glow.setColorAt(1.0, QColor(252, 238, 10, 8))
        painter.fillRect(self.rect(), glow)

        # 2. Cyberpunk edge border pulsing
        border_pen = QPen(QColor(CYBER_YELLOW), 3)
        painter.setPen(border_pen)
        painter.drawRect(2, 2, w - 4, h - 4)

        # 3. Motion blur / Sandevistan afterimage lightning trails
        n = len(self.trail_points)
        for i in range(n - 1):
            p1 = self.trail_points[i]
            p2 = self.trail_points[i + 1]
            ratio = (i + 1) / float(n)
            alpha = int(240 * ratio)
            thick = max(1.5, ratio * 9.0)

            # Neon Green core with Cyan glow
            color = QColor(0, 255, 102, alpha) if i % 2 == 0 else QColor(0, 240, 255, alpha)
            painter.setPen(QPen(color, thick, Qt.SolidLine, Qt.RoundCap))
            painter.drawLine(p1, p2)

            # Ghost chromatic ghost particle
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor(252, 238, 10, int(alpha * 0.7)))
            painter.drawEllipse(p2, int(thick * 0.8), int(thick * 0.8))

        painter.end()


class CyberGlitchOverlay(QWidget):
    """Full-window cybernetic glitch burst overlay triggered on game launch"""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WA_TransparentForMouseEvents, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.is_glitching = False
        self.glitch_step = 0
        self.total_steps = 28  # ~28 frames * 35ms ~= 1.0 second
        self.game_name = ""

        self.timer = QTimer(self)
        self.timer.setInterval(35)
        self.timer.timeout.connect(self._on_tick)

    def trigger_burst(self, game_name="GAME"):
        self.game_name = str(game_name).upper()
        self.is_glitching = True
        self.glitch_step = self.total_steps
        self.timer.start()
        self.update()

    def _on_tick(self):
        self.glitch_step -= 1
        if self.glitch_step <= 0:
            self.timer.stop()
            self.is_glitching = False
        self.update()

    def paintEvent(self, event):
        if not self.is_glitching or self.glitch_step <= 0:
            return

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, False)
        w, h = self.width(), self.height()
        ratio = self.glitch_step / float(self.total_steps)
        alpha = int(220 * ratio)

        # 1. Random horizontal glitch color slices
        num_slices = random.randint(4, 9)
        colors = [
            QColor(0, 240, 255, int(alpha * 0.75)),   # Cyan
            QColor(252, 238, 10, int(alpha * 0.8)),   # Yellow
            QColor(255, 0, 60, int(alpha * 0.7)),     # Red
            QColor(0, 255, 102, int(alpha * 0.6)),    # Green
        ]

        for _ in range(num_slices):
            sy = random.randint(0, max(1, h - 30))
            sh = random.randint(4, 30)
            sx_offset = random.randint(-40, 40)
            color = random.choice(colors)
            painter.fillRect(QRect(sx_offset, sy, w + abs(sx_offset), sh), color)

        # 2. Cyber scanlines flicker
        scan_pen = QPen(QColor(0, 240, 255, int(alpha * 0.25)), 1)
        painter.setPen(scan_pen)
        for y in range(0, h, 8):
            if random.random() > 0.35:
                painter.drawLine(0, y, w, y)

        # 3. Flashing Cyberpunk Diagnostic HUD text
        font = QFont("Impact", 28, QFont.Bold)
        font.setLetterSpacing(QFont.AbsoluteSpacing, 3)
        painter.setFont(font)

        # Chromatic split text: Cyan + Red + Yellow
        msg = f"⚡ INITIALIZING: {self.game_name} ⚡"
        dx = random.randint(-5, 5)
        dy = random.randint(-3, 3)

        rect = self.rect()
        painter.setPen(QColor(0, 240, 255, alpha))
        painter.drawText(rect.adjusted(dx - 3, dy - 2, dx - 3, dy - 2), Qt.AlignCenter, msg)
        painter.setPen(QColor(255, 0, 60, alpha))
        painter.drawText(rect.adjusted(dx + 3, dy + 2, dx + 3, dy + 2), Qt.AlignCenter, msg)
        painter.setPen(QColor(252, 238, 10, min(255, alpha + 35)))
        painter.drawText(rect.adjusted(dx, dy, dx, dy), Qt.AlignCenter, msg)

        # Sub-telemetry text
        sub_font = QFont("Consolas", 11, QFont.Bold)
        painter.setFont(sub_font)
        painter.setPen(QColor(0, 255, 102, alpha))
        sub_msg = f"// NEURAL INTERFACE LOCKED // DISCORD PRESENCE ACTIVE // 0x{random.randint(100000, 999999):X}"
        painter.drawText(rect.adjusted(0, 60, 0, 60), Qt.AlignCenter, sub_msg)

        painter.end()


class MainWindow(QMainWindow):
    def __init__(self, spoofer_engine, icon_path=None):
        super().__init__()
        self.spoofer = spoofer_engine
        self.icon_path = icon_path

        # Frameless Cyberpunk Window - NO WHITE BORDERS!
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.resize(1060, 760)
        self.setMinimumSize(850, 600)

        self.drag_position = QPoint()
        self.sandevistan_active = False
        self.sandevistan_trail_points = []

        # Filesystem & Persistence setup
        if getattr(sys, 'frozen', False):
            self.app_dir = os.path.dirname(sys.executable)
            self.res_dir = getattr(sys, '_MEIPASS', self.app_dir)
        else:
            self.app_dir = os.path.dirname(os.path.abspath(__file__))
            self.res_dir = self.app_dir

        self.db_path = os.path.join(self.app_dir, "games_db.json")
        self.settings_path = os.path.join(self.app_dir, "settings.json")
        self.settings = self.load_settings()

        # UI Settings
        self.ui_opacity = max(0.1, min(0.95, self.settings.get("opacity", 75) / 100.0))
        self.saved_volume = int(self.settings.get("volume", 80))
        self.current_bg_path = self.settings.get("background_path", "")

        # Games DB setup
        self.DEFAULT_ALLOWED_IDS = {
            "cyberpunk2077", "endfield", "pragmata", "re_requiem",
            "wwm", "genshin", "hsr", "roblox", "forest3",
            "aniimo", "forgotten_island", "marvel_rivals", "rust"
        }
        self.games = self.load_games()
        self.cards = {}

        # Auto-updater for Discord detectable games database
        self.bg_db_updater = DiscordDatabaseUpdater(self._get_detectable_db_path(), self)
        self.bg_db_updater.update_finished.connect(self._on_bg_db_updated)
        QTimer.singleShot(2500, self.bg_db_updater.start)

        # Video Player setup (Direct QMediaPlayer looping without frozen QMediaPlaylist)
        self.player = QMediaPlayer(self)
        self.player.mediaStatusChanged.connect(self._on_media_status_changed)

        self.init_ui()
        self.setup_signals()

        # Defer background initialization to after the event loop starts
        QTimer.singleShot(150, self.init_background)

        # Sandevistan pulse timer
        self.sandevistan_timer = QTimer(self)
        self.sandevistan_timer.setInterval(30)
        self.sandevistan_timer.timeout.connect(self._sandevistan_tick)

    def load_settings(self):
        settings = {
            "volume": 80,
            "opacity": 75,
            "background_path": ""
        }
        if os.path.exists(self.settings_path):
            try:
                with open(self.settings_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        settings.update(data)
            except Exception as e:
                print(f"Error loading settings: {e}")
        return settings

    def save_settings(self):
        try:
            data = {
                "volume": self.slider_vol.value() if hasattr(self, 'slider_vol') else self.saved_volume,
                "opacity": int(self.ui_opacity * 100),
                "background_path": getattr(self, 'current_bg_path', "")
            }
            with open(self.settings_path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")

    def load_games(self):
        default_list = [
            {
                "id": "cyberpunk2077",
                "name": "Cyberpunk 2077",
                "client_id": "787443973538971748",
                "process": "Cyberpunk2077.exe",
                "path_rel": "Cyberpunk 2077/bin/x64/Cyberpunk2077.exe",
                "window_title": "Cyberpunk 2077",
                "category": "Action RPG",
                "duration_minutes": 15,
                "description": "Discord Quest for Night City Orbs & Edgerunner Drops",
                "accent_color": "#FCEE0A"
            },
            {
                "id": "endfield",
                "name": "Arknights: Endfield",
                "client_id": "1461154307171811401",
                "process": "Endfield.exe",
                "path_rel": "Arknights Endfield/Endfield.exe",
                "window_title": "Arknights: Endfield",
                "category": "3D RPG",
                "duration_minutes": 15,
                "description": "Discord Quest for Talos-II Drops & Orbs",
                "accent_color": "#00F0FF"
            },
            {
                "id": "pragmata",
                "name": "Pragmata",
                "client_id": "1448369915462549616",
                "process": "pragmata_sketchbook.exe",
                "path_rel": "PRAGMATA/pragmata_sketchbook.exe",
                "window_title": "PRAGMATA",
                "category": "Capcom / Sci-Fi",
                "duration_minutes": 15,
                "description": "Discord Quest for Lunar Drops & Orbs",
                "accent_color": "#FFB300"
            },
            {
                "id": "re_requiem",
                "name": "Resident Evil Requiem",
                "client_id": "1456485028350656512",
                "process": "re9.exe",
                "path_rel": "Resident Evil Requiem/re9.exe",
                "window_title": "Resident Evil Requiem",
                "category": "Capcom / Horror",
                "duration_minutes": 15,
                "description": "Discord Quest for Umbrella Drops & Orbs",
                "accent_color": "#FF003C"
            },
            {
                "id": "wwm",
                "name": "Where Winds Meet",
                "client_id": "1437509662303059998",
                "process": "wwm.exe",
                "path_rel": "Where Winds Meet/Engine/Binaries/Win64r/wwm.exe",
                "window_title": "Where Winds Meet",
                "category": "Action RPG",
                "duration_minutes": 15,
                "description": "Discord Quest for In-Game Drops & Orbs",
                "accent_color": "#00F0FF"
            },
            {
                "id": "genshin",
                "name": "Genshin Impact",
                "client_id": "762434991303950386",
                "process": "GenshinImpact.exe",
                "path_rel": "Genshin Impact/Genshin Impact game/GenshinImpact.exe",
                "window_title": "Genshin Impact",
                "category": "HoYoverse",
                "duration_minutes": 15,
                "description": "Discord Quest for Primogems & Orbs",
                "accent_color": "#00F0FF"
            },
            {
                "id": "hsr",
                "name": "Honkai: Star Rail",
                "client_id": "1121201675240210523",
                "process": "StarRail.exe",
                "path_rel": "Honkai Star Rail/Games/StarRail.exe",
                "window_title": "Honkai: Star Rail",
                "category": "HoYoverse",
                "duration_minutes": 15,
                "description": "Discord Quest for Stellar Jades & Orbs",
                "accent_color": "#D070FF"
            },
            {
                "id": "roblox",
                "name": "Roblox",
                "client_id": "363445589247131668",
                "process": "RobloxPlayerBeta.exe",
                "path_rel": "Roblox/Versions/version-client/RobloxPlayerBeta.exe",
                "window_title": "Roblox",
                "category": "Sandbox",
                "duration_minutes": 15,
                "description": "Discord Quest for Avatar Items & Orbs",
                "accent_color": "#00A2FF"
            },
            {
                "id": "forest3",
                "name": "Endnight Debuts Forest 3",
                "client_id": None,
                "process": "EndnightDebutsForest3.exe",
                "path_rel": "Endnight Debuts Forest 3/EndnightDebutsForest3.exe",
                "window_title": "Endnight Debuts Forest 3",
                "category": "Survival / Horror",
                "duration_minutes": 15,
                "description": "Discord Quest: Endnight Games Survival Horror Simulation",
                "accent_color": "#FF003C"
            },
            {
                "id": "aniimo",
                "name": "ANIIMO GLOBAL LAUNCH",
                "client_id": "1468082130474111047",
                "process": "aniimo.exe",
                "path_rel": "Aniimo/aniimo.exe",
                "window_title": "Aniimo",
                "category": "Creature RPG / Quest",
                "duration_minutes": 15,
                "description": "Discord Quest для ANIIMO GLOBAL LAUNCH (Orbs & In-Game Drops)",
                "accent_color": "#00F0FF",
                "extra_executables": [
                    "win64/aniimo.exe",
                    "aniimo.exe"
                ]
            },
            {
                "id": "forgotten_island",
                "name": "FORGOTTEN ISLAND",
                "client_id": "1468199201984217088",
                "process": "forgottenisland.exe",
                "path_rel": "Forgotten Island/forgottenisland.exe",
                "window_title": "Forgotten Island",
                "category": "Adventure / Quest",
                "duration_minutes": 15,
                "description": "Discord Quest для FORGOTTEN ISLAND (Rewards & Orbs)",
                "accent_color": "#FCEE0A",
                "extra_executables": [
                    "win64/forgottenisland-win64-shipping.exe",
                    "win64/forgottenisland.exe",
                    "forgottenisland.exe"
                ]
            }
        ]
        path_to_try = self.db_path
        if not os.path.exists(path_to_try):
            bundled = os.path.join(self.res_dir, "games_db.json")
            if os.path.exists(bundled):
                path_to_try = bundled

        if os.path.exists(path_to_try):
            try:
                with open(path_to_try, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    filtered = list(loaded)
                    existing_map = {g.get("id"): g for g in filtered}
                    # Update standard fields from default_list
                    for d in default_list:
                        gid = d["id"]
                        if gid in existing_map:
                            existing_map[gid].update({
                                "client_id": d.get("client_id"),
                                "process": d["process"],
                                "path_rel": d["path_rel"],
                                "window_title": d["window_title"]
                            })
                            if "extra_executables" in d:
                                existing_map[gid]["extra_executables"] = d["extra_executables"]
                        else:
                            filtered.append(d)
                    return filtered
            except Exception as e:
                print(f"Error loading games: {e}")
        return default_list

    def _get_detectable_db_path(self):
        candidates = [
            os.path.join(self.app_dir, "discord_detectable.json"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "discord_detectable.json")
        ]
        for c in candidates:
            try:
                if os.path.exists(c):
                    with open(c, "a"):
                        pass
                    return c
            except Exception:
                pass
        fallback = os.path.join(os.path.expanduser("~"), ".eshkeri", "discord_detectable.json")
        os.makedirs(os.path.dirname(fallback), exist_ok=True)
        return fallback

    def _on_bg_db_updated(self, success, count, msg):
        if success:
            print(f"[Discord Database Auto-Updater] Updated: {count} detectable games available.")

    def save_games(self):
        try:
            with open(self.db_path, "w", encoding="utf-8") as f:
                json.dump(self.games, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"Error saving games: {e}")

    def init_ui(self):
        # 1. QGraphicsScene and QGraphicsView container
        self.scene = QGraphicsScene(self)
        self.view = QGraphicsView(self.scene, self)
        self.view.setFrameShape(QGraphicsView.NoFrame)
        self.view.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.view.setStyleSheet("background: #090C12; border: none;")
        self.setCentralWidget(self.view)

        # 2. QGraphicsVideoItem for background video
        self.video_item = QGraphicsVideoItem()
        self.video_item.setSize(QSizeF(self.width(), self.height()))
        self.scene.addItem(self.video_item)
        self.player.setVideoOutput(self.video_item)

        # 2b. QGraphicsPixmapItem for image background
        self.pixmap_item = QGraphicsPixmapItem()
        self.scene.addItem(self.pixmap_item)
        self.pixmap_item.setVisible(False)

        # 3. Transparent UI Overlay Widget
        self.ui_widget = QWidget()
        self.ui_widget.resize(self.width(), self.height())
        self.ui_widget.setStyleSheet("background: transparent;")

        main_layout = QVBoxLayout(self.ui_widget)
        main_layout.setContentsMargins(16, 12, 16, 14)
        main_layout.setSpacing(10)

        # 4. TOP TITLE BAR (Window Controls)
        title_bar = QFrame()
        title_bar_layout = QHBoxLayout(title_bar)
        title_bar_layout.setContentsMargins(8, 2, 8, 2)
        title_bar_layout.setSpacing(10)

        # Logo + Title
        lbl_app = QLabel("⚡ ESHKE•RI")
        lbl_app.setFont(QFont("Impact", 20))
        lbl_app.setStyleSheet(f"color: {CYBER_YELLOW}; letter-spacing: 2px;")
        title_bar_layout.addWidget(lbl_app)

        lbl_ver = QLabel("// CYBERPUNK 2077 HUD")
        lbl_ver.setFont(QFont("Consolas", 10, QFont.Bold))
        lbl_ver.setStyleSheet(f"color: {CYBER_CYAN};")
        title_bar_layout.addWidget(lbl_ver)

        title_bar_layout.addStretch()

        # Sandevistan Overdrive Button
        self.btn_sandevistan = CyberGlitchButton("⚡ SANDEVISTAN [OFF]")
        self.btn_sandevistan.clicked.connect(self.toggle_sandevistan)
        title_bar_layout.addWidget(self.btn_sandevistan)

        # Discord Status Chip
        self.chip_discord = QLabel("DISCORD: ПРОВЕРКА...")
        self.chip_discord.setFont(QFont("Consolas", 10, QFont.Bold))
        self.chip_discord.setStyleSheet("color: #FFFFFF; background: rgba(32, 38, 54, 210); border: 1px solid #4A5568; padding: 4px 10px; border-radius: 2px;")
        title_bar_layout.addWidget(self.chip_discord)

        # Window Action Buttons
        btn_min = QPushButton("—")
        btn_min.setFixedSize(32, 28)
        btn_min.setStyleSheet("color: #FFFFFF; background: transparent; border: none; font-size: 15px; font-weight: bold;")
        btn_min.clicked.connect(self.showMinimized)
        title_bar_layout.addWidget(btn_min)

        btn_close = QPushButton("✕")
        btn_close.setFixedSize(32, 28)
        btn_close.setStyleSheet("color: #FF003C; background: transparent; border: none; font-size: 16px; font-weight: bold;")
        btn_close.clicked.connect(self.close)
        title_bar_layout.addWidget(btn_close)

        main_layout.addWidget(title_bar)

        # 5. SETTINGS PANEL (Video Background, Volume, Opacity)
        self.settings_panel = QFrame()
        set_layout = QHBoxLayout(self.settings_panel)
        set_layout.setContentsMargins(12, 6, 12, 6)
        set_layout.setSpacing(14)

        # Video Selector
        lbl_v = QLabel("🎥 Фон:")
        lbl_v.setFont(QFont("Consolas", 10, QFont.Bold))
        lbl_v.setStyleSheet(f"color: {CYBER_CYAN};")
        set_layout.addWidget(lbl_v)

        self.combo_videos = QComboBox()
        self.combo_videos.setStyleSheet("""
            QComboBox {
                background: #0B101A;
                color: #FFFFFF;
                border: 1px solid #00F0FF;
                padding: 4px 8px;
                font-family: Consolas;
                font-size: 11px;
                min-width: 180px;
            }
            QComboBox QAbstractItemView {
                background: #0B101A;
                color: #FFFFFF;
                selection-background-color: #00F0FF;
                selection-color: #000000;
            }
        """)
        self.combo_videos.currentIndexChanged.connect(self._on_video_selected)
        set_layout.addWidget(self.combo_videos)

        btn_browse_vid = QPushButton("📂 Выбрать")
        btn_browse_vid.setStyleSheet("background: #172132; color: #00F0FF; border: 1px solid #00F0FF; font-size: 11px; padding: 4px 8px;")
        btn_browse_vid.clicked.connect(self.browse_background_file)
        set_layout.addWidget(btn_browse_vid)

        # Volume Slider
        lbl_vol = QLabel("🔊 Звук:")
        lbl_vol.setFont(QFont("Consolas", 10, QFont.Bold))
        lbl_vol.setStyleSheet(f"color: {CYBER_YELLOW};")
        set_layout.addWidget(lbl_vol)

        self.slider_vol = QSlider(Qt.Horizontal)
        self.slider_vol.setRange(0, 100)
        self.slider_vol.setValue(self.saved_volume)
        self.slider_vol.setFixedWidth(90)
        self.slider_vol.setStyleSheet(f"""
            QSlider::groove:horizontal {{ height: 4px; background: #202636; border-radius: 2px; }}
            QSlider::sub-page:horizontal {{ background: {CYBER_YELLOW}; border-radius: 2px; }}
            QSlider::handle:horizontal {{ background: #FFFFFF; border: 1px solid {CYBER_YELLOW}; width: 12px; margin-top: -4px; margin-bottom: -4px; border-radius: 6px; }}
        """)
        self.slider_vol.valueChanged.connect(self.set_volume)
        set_layout.addWidget(self.slider_vol)

        self.lbl_vol_val = QLabel(f"{self.saved_volume}%")
        self.lbl_vol_val.setFont(QFont("Consolas", 10))
        self.lbl_vol_val.setStyleSheet(f"color: {CYBER_YELLOW}; min-width: 30px;")
        set_layout.addWidget(self.lbl_vol_val)

        # Interface Opacity Slider (Transparency)
        lbl_op = QLabel("👁 Прозрачность:")
        lbl_op.setFont(QFont("Consolas", 10, QFont.Bold))
        lbl_op.setStyleSheet(f"color: {CYBER_MAGENTA};")
        set_layout.addWidget(lbl_op)

        self.slider_opacity = QSlider(Qt.Horizontal)
        self.slider_opacity.setRange(10, 95)
        self.slider_opacity.setValue(int(self.ui_opacity * 100))
        self.slider_opacity.setFixedWidth(90)
        self.slider_opacity.setStyleSheet(f"""
            QSlider::groove:horizontal {{ height: 4px; background: #202636; border-radius: 2px; }}
            QSlider::sub-page:horizontal {{ background: {CYBER_MAGENTA}; border-radius: 2px; }}
            QSlider::handle:horizontal {{ background: #FFFFFF; border: 1px solid {CYBER_MAGENTA}; width: 12px; margin-top: -4px; margin-bottom: -4px; border-radius: 6px; }}
        """)
        self.slider_opacity.valueChanged.connect(self.set_ui_transparency)
        set_layout.addWidget(self.slider_opacity)

        self.lbl_op_val = QLabel(f"{int(self.ui_opacity * 100)}%")
        self.lbl_op_val.setFont(QFont("Consolas", 10))
        self.lbl_op_val.setStyleSheet(f"color: {CYBER_MAGENTA}; min-width: 30px;")
        set_layout.addWidget(self.lbl_op_val)

        set_layout.addStretch()
        main_layout.addWidget(self.settings_panel)

        # 6. ACTIVE QUEST HUD PANEL
        self.hud_panel = QFrame()
        hud_layout = QVBoxLayout(self.hud_panel)
        hud_layout.setContentsMargins(16, 12, 16, 12)
        hud_layout.setSpacing(8)

        top_hud = QHBoxLayout()
        self.lbl_hud_status = QLabel("STATUS: [STANDBY] // ВЫБЕРИТЕ ИГРУ ИЗ СПИСКА ДЛЯ КВЕСТА")
        self.lbl_hud_status.setFont(QFont("Consolas", 11, QFont.Bold))
        self.lbl_hud_status.setStyleSheet(f"color: {CYBER_CYAN};")
        top_hud.addWidget(self.lbl_hud_status)
        top_hud.addStretch()

        self.lbl_fps = QLabel("")
        self.lbl_fps.setFont(QFont("Consolas", 11, QFont.Bold))
        self.lbl_fps.setStyleSheet("color: #00FF66; background: rgba(0, 255, 102, 25); border: 1px solid rgba(0, 255, 102, 80); padding: 3px 8px; border-radius: 2px;")
        self.lbl_fps.hide()
        top_hud.addWidget(self.lbl_fps)

        self.lbl_timer = QLabel("15:00")
        self.lbl_timer.setFont(QFont("Consolas", 18, QFont.Bold))
        self.lbl_timer.setStyleSheet(f"color: {CYBER_YELLOW};")
        top_hud.addWidget(self.lbl_timer)

        self.btn_stop = CyberGlitchButton("⏹ ОСТАНОВИТЬ", is_red=True)
        self.btn_stop.setEnabled(False)
        self.btn_stop.clicked.connect(self.spoofer.stop)
        top_hud.addWidget(self.btn_stop)

        hud_layout.addLayout(top_hud)

        # Animated Progress Bar
        self.progress_frame = QFrame()
        self.progress_frame.setFixedHeight(10)
        self.progress_frame.setStyleSheet("background: rgba(10, 14, 22, 220); border-radius: 2px; border: 1px solid rgba(0, 240, 255, 80);")
        self.progress_fill = QFrame(self.progress_frame)
        self.progress_fill.setGeometry(0, 0, 0, 10)
        self.progress_fill.setStyleSheet(f"background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {CYBER_CYAN}, stop:1 {CYBER_YELLOW}); border-radius: 2px;")
        hud_layout.addWidget(self.progress_frame)

        self.lbl_hud_details = QLabel("При запуске симуляции открывается реальное окно игры, которое Discord распознает для квеста.")
        self.lbl_hud_details.setStyleSheet("color: #CBD5E1; font-size: 11px;")
        hud_layout.addWidget(self.lbl_hud_details)

        main_layout.addWidget(self.hud_panel)

        # 7. SEARCH & ADD BAR
        ctrl_layout = QHBoxLayout()
        ctrl_layout.setSpacing(10)

        self.search_in = QLineEdit()
        self.search_in.setPlaceholderText("🔍 Поиск игры по названию или .exe...")
        self.search_in.setStyleSheet(f"""
            QLineEdit {{
                background: rgba(11, 16, 26, 220);
                border: 1px solid {CYBER_CYAN};
                color: #FFFFFF;
                padding: 6px 12px;
                font-family: Consolas;
                font-size: 12px;
                border-radius: 2px;
            }}
            QLineEdit:focus {{
                border: 2px solid {CYBER_YELLOW};
            }}
        """)
        self.search_in.textChanged.connect(self.filter_games)
        ctrl_layout.addWidget(self.search_in, stretch=1)

        btn_add = CyberGlitchButton("➕ ДОБАВИТЬ НОВУЮ ИГРУ", is_yellow=True)
        btn_add.clicked.connect(self.show_add_game_dialog)
        ctrl_layout.addWidget(btn_add)

        main_layout.addLayout(ctrl_layout)

        # 8. GAMES LIST SCROLL AREA
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("QScrollArea { border: none; background: transparent; }")

        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet("background: transparent;")
        self.games_layout = QVBoxLayout(self.scroll_content)
        self.games_layout.setContentsMargins(0, 0, 0, 0)
        self.games_layout.setSpacing(8)

        scroll.setWidget(self.scroll_content)
        main_layout.addWidget(scroll, stretch=1)

        # Add UI to scene as proxy widget
        self.ui_proxy = self.scene.addWidget(self.ui_widget)
        self.ui_proxy.setPos(0, 0)

        # Sandevistan Top Overlay
        self.sandevistan_overlay = SandevistanOverlay(self)
        self.sandevistan_overlay.resize(self.width(), self.height())
        self.sandevistan_overlay.raise_()

        # CyberGlitch Launch Burst Overlay
        self.glitch_overlay = CyberGlitchOverlay(self)
        self.glitch_overlay.resize(self.width(), self.height())
        self.glitch_overlay.raise_()

        self.apply_theme_colors()
        self.render_games()

    def apply_theme_colors(self):
        alpha = int(self.ui_opacity * 255)
        self.settings_panel.setStyleSheet(f"background: rgba(14, 20, 32, {alpha}); border: 1px solid rgba(0, 240, 255, 120); border-radius: 4px;")
        self.hud_panel.setStyleSheet(f"background: rgba(14, 20, 32, {alpha}); border: 2px solid {CYBER_CYAN}; border-radius: 4px;")
        for card in self.cards.values():
            card.update_style()

    def init_background(self):
        user_home = os.path.expanduser("~")
        fonpril_app = os.path.join(self.app_dir, "fonpril.mp4")
        fonpril_cur = os.path.join(os.getcwd(), "fonpril.mp4")
        preferred_video = os.path.join(user_home, "Videos", "opening cyberpunck.mp4")
        
        search_dirs = [
            self.app_dir,
            os.path.join(user_home, "Videos"),
            os.path.join(user_home, "Downloads"),
        ]
        
        media_files = []
        if os.path.exists(fonpril_app):
            media_files.append(fonpril_app)
        elif os.path.exists(fonpril_cur):
            media_files.append(fonpril_cur)

        if self.current_bg_path and os.path.exists(self.current_bg_path) and self.current_bg_path not in media_files:
            media_files.append(self.current_bg_path)

        if os.path.exists(preferred_video) and preferred_video not in media_files:
            media_files.append(preferred_video)
            
        for sdir in search_dirs:
            if sdir and os.path.exists(sdir):
                for ext in ("*.mp4", "*.webm", "*.mkv", "*.avi", "*.png", "*.jpg", "*.jpeg", "*.webp", "*.bmp"):
                    for mf in glob.glob(os.path.join(sdir, ext)):
                        if mf not in media_files:
                            media_files.append(mf)

        self.media_files = media_files
        self.combo_videos.blockSignals(True)
        self.combo_videos.clear()

        default_index = 0
        for i, mf in enumerate(media_files):
            basename = os.path.basename(mf)
            self.combo_videos.addItem(basename, mf)
            if self.current_bg_path and mf == self.current_bg_path:
                default_index = i
            elif not self.current_bg_path and "fonpril" in basename.lower():
                default_index = i

        self.combo_videos.blockSignals(False)

        if media_files:
            self.combo_videos.setCurrentIndex(default_index)
            self.set_background(media_files[default_index])
        else:
            self.combo_videos.addItem("Нет медиафайлов", "")

    def set_background(self, path):
        if not path or not os.path.exists(path):
            return
        self.current_bg_path = path
        ext = os.path.splitext(path)[1].lower()
        is_image = ext in (".png", ".jpg", ".jpeg", ".webp", ".bmp")

        if is_image:
            self.player.stop()
            self.video_item.setVisible(False)
            self.pixmap_item.setVisible(True)
            self._update_image_background()
        else:
            self.pixmap_item.setVisible(False)
            self.video_item.setVisible(True)
            self.play_video(path)

        self.save_settings()

    def _update_image_background(self):
        if hasattr(self, 'pixmap_item') and self.pixmap_item.isVisible() and getattr(self, 'current_bg_path', None):
            orig = QPixmap(self.current_bg_path)
            if not orig.isNull():
                scaled = orig.scaled(
                    self.width(), self.height(),
                    Qt.KeepAspectRatioByExpanding,
                    Qt.SmoothTransformation
                )
                dx = int((self.width() - scaled.width()) / 2)
                dy = int((self.height() - scaled.height()) / 2)
                self.pixmap_item.setPixmap(scaled)
                self.pixmap_item.setPos(dx, dy)

    def play_video(self, path):
        if path and os.path.exists(path):
            try:
                self.current_video_path = path
                self.player.setMedia(QMediaContent(QUrl.fromLocalFile(path)))
                self.player.setVolume(self.slider_vol.value())
                self.player.play()
            except Exception as e:
                print(f"Error playing video {path}: {e}")

    def _on_media_status_changed(self, status):
        # Auto-loop video cleanly when it reaches the end or stops
        if status in (QMediaPlayer.EndOfMedia, QMediaPlayer.LoadedMedia):
            if status == QMediaPlayer.EndOfMedia:
                self.player.setPosition(0)
                self.player.play()

    def _on_video_selected(self, index):
        mf = self.combo_videos.currentData()
        if mf:
            self.set_background(mf)

    def browse_background_file(self):
        downloads_dir = os.path.join(os.path.expanduser("~"), "Downloads")
        fn, _ = QFileDialog.getOpenFileName(
            self, "Выбрать файл для фона (видео или картинку)", downloads_dir,
            "Файлы фона (*.mp4 *.webm *.mkv *.avi *.png *.jpg *.jpeg *.webp *.bmp);;Видео (*.mp4 *.webm *.mkv *.avi);;Изображения (*.png *.jpg *.jpeg *.webp *.bmp);;Все файлы (*.*)"
        )
        if fn:
            basename = os.path.basename(fn)
            self.combo_videos.blockSignals(True)
            self.combo_videos.insertItem(0, basename, fn)
            self.combo_videos.setCurrentIndex(0)
            self.combo_videos.blockSignals(False)
            self.set_background(fn)

    def set_volume(self, val):
        self.lbl_vol_val.setText(f"{val}%")
        self.player.setVolume(val)
        self.save_settings()

    def set_ui_transparency(self, val):
        self.lbl_op_val.setText(f"{val}%")
        self.ui_opacity = val / 100.0
        self.apply_theme_colors()
        self.save_settings()

    def toggle_sandevistan(self):
        self.sandevistan_active = not self.sandevistan_active
        self.sandevistan_overlay.is_active = self.sandevistan_active
        if self.sandevistan_active:
            self.btn_sandevistan.setText("⚡ SANDEVISTAN [ACTIVE]")
            self.btn_sandevistan.is_yellow = True
            self.btn_sandevistan._update_stylesheet()
            self.sandevistan_timer.start()
        else:
            self.btn_sandevistan.setText("⚡ SANDEVISTAN [OFF]")
            self.btn_sandevistan.is_yellow = False
            self.btn_sandevistan._update_stylesheet()
            self.sandevistan_timer.stop()
            self.sandevistan_trail_points.clear()
            self.sandevistan_overlay.trail_points.clear()
            self.sandevistan_overlay.update()

    def _sandevistan_tick(self):
        pos = self.mapFromGlobal(QCursor.pos())
        self.sandevistan_trail_points.append(pos)
        if len(self.sandevistan_trail_points) > 24:
            self.sandevistan_trail_points.pop(0)
        self.sandevistan_overlay.trail_points = list(self.sandevistan_trail_points)
        self.sandevistan_overlay.update()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.pos().y() < 55:
            self.drag_position = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    def mouseMoveEvent(self, event):
        if event.buttons() == Qt.LeftButton and not self.drag_position.isNull():
            self.move(event.globalPos() - self.drag_position)
            event.accept()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.drag_position = QPoint()
        super().mouseReleaseEvent(event)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        w, h = self.width(), self.height()
        self.scene.setSceneRect(0, 0, w, h)
        self.video_item.setSize(QSizeF(w, h))
        self.ui_widget.resize(w, h)
        if hasattr(self, 'sandevistan_overlay'):
            self.sandevistan_overlay.resize(w, h)
            self.sandevistan_overlay.raise_()
        if self.spoofer.is_running and self.spoofer.target_seconds > 0:
            pct = min(1.0, self.spoofer.elapsed_seconds / float(self.spoofer.target_seconds))
            bw = int(self.progress_frame.width() * pct)
            self.progress_fill.setGeometry(0, 0, bw, 10)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)

        w, h = self.width(), self.height()

        # Outer Cyberpunk Border (No white borders!)
        border_pen = QPen(QColor(CYBER_YELLOW if self.sandevistan_active else CYBER_CYAN), 2)
        painter.setPen(border_pen)

        path = QPainterPath()
        path.moveTo(20, 2)
        path.lineTo(w - 2, 2)
        path.lineTo(w - 2, h - 20)
        path.lineTo(w - 20, h - 2)
        path.lineTo(2, h - 2)
        path.lineTo(2, 20)
        path.closeSubpath()
        painter.drawPath(path)

        # Sandevistan Ghost Motion Trails
        if self.sandevistan_active and len(self.sandevistan_trail_points) > 1:
            for i in range(len(self.sandevistan_trail_points) - 1):
                p1 = self.sandevistan_trail_points[i]
                p2 = self.sandevistan_trail_points[i + 1]
                alpha = int(255 * (i / float(len(self.sandevistan_trail_points))))
                color = QColor(0, 255, 102, alpha) if i % 2 == 0 else QColor(0, 240, 255, alpha)
                painter.setPen(QPen(color, (i + 1) * 0.7, Qt.SolidLine, Qt.RoundCap))
                painter.drawLine(p1, p2)

        painter.end()

    def render_games(self, query=""):
        for i in reversed(range(self.games_layout.count())):
            w = self.games_layout.itemAt(i).widget()
            if w:
                w.setParent(None)

        self.cards.clear()
        query = query.lower().strip()

        active_id = self.spoofer.active_game.get("id") if (self.spoofer.is_running and self.spoofer.active_game) else None

        for game in self.games:
            name = game.get("name", "").lower()
            proc = game.get("process", "").lower()
            if query and (query not in name and query not in proc):
                continue

            card = GameCard(
                game,
                is_active=(game.get("id") == active_id),
                get_opacity_fn=lambda: self.ui_opacity
            )
            card.start_requested.connect(self.start_game)
            card.delete_requested.connect(self.delete_game)
            self.games_layout.addWidget(card)
            self.cards[game.get("id")] = card

        self.games_layout.addStretch()

    def filter_games(self, text):
        self.render_games(text)

    def show_add_game_dialog(self):
        dlg = AddGameDialog(self)
        if dlg.exec_() == QDialog.Accepted and dlg.game_data:
            self.games.insert(0, dlg.game_data)
            self.save_games()
            self.render_games(self.search_in.text())
            QMessageBox.information(self, "Успех", f"Игра '{dlg.game_data['name']}' добавлена!")

    def delete_game(self, game_id):
        reply = QMessageBox.question(
            self, "Удаление", "Удалить эту игру?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            self.games = [g for g in self.games if g.get("id") != game_id]
            self.save_games()
            self.render_games(self.search_in.text())

    def start_game(self, game_dict):
        if hasattr(self, 'glitch_overlay'):
            self.glitch_overlay.trigger_burst(game_dict.get("name", "GAME"))
        self.spoofer.start(game_dict)

    def setup_signals(self):
        self.spoofer.discord_status.connect(self.on_discord_status)
        self.spoofer.status_changed.connect(self.on_spoofer_status_changed)
        self.spoofer.tick.connect(self.on_spoofer_tick)
        self.spoofer.quest_completed.connect(self.on_quest_completed)

    def on_discord_status(self, is_running):
        if is_running:
            self.chip_discord.setText("DISCORD: АКТИВЕН ✔")
            self.chip_discord.setStyleSheet(f"color: #000000; background: {CYBER_GREEN}; font-weight: bold; padding: 4px 10px; border-radius: 2px;")
        else:
            self.chip_discord.setText("DISCORD: НЕ ЗАПУЩЕН ✖")
            self.chip_discord.setStyleSheet(f"color: {CYBER_RED}; background: rgba(32, 16, 21, 220); border: 1px solid {CYBER_RED}; font-weight: bold; padding: 4px 10px; border-radius: 2px;")

    def on_spoofer_status_changed(self, is_running, game_name):
        self.btn_stop.setEnabled(is_running)

        if is_running:
            self.lbl_hud_status.setText(f"STATUS: [ACTIVE] // ВЫПОЛНЯЕТСЯ КВЕСТ: {game_name.upper()}")
            self.lbl_hud_status.setStyleSheet(f"color: {CYBER_YELLOW};")
            self.lbl_hud_details.setText(
                "✔ Окно игры и системные процессы запущены! Discord фиксирует игровое время.\n"
                "💡 ВАЖНО ДЛЯ ЗАЧЕТА: 1) В Discord нажмите «Принять квест» (Quests). "
                "2) В Discord: Настройки -> Конфиденциальность активности -> включите «Отображать активность»."
            )
            self.lbl_fps.setText("⚡ 144 FPS")
            self.lbl_fps.show()
        else:
            self.lbl_hud_status.setText("STATUS: [STANDBY] // ВЫБЕРИТЕ ИГРУ ИЗ СПИСКА")
            self.lbl_hud_status.setStyleSheet(f"color: {CYBER_CYAN};")
            self.lbl_timer.setText("15:00")
            self.lbl_fps.hide()
            self.progress_fill.setGeometry(0, 0, 0, 10)
            self.lbl_hud_details.setText("При запуске симуляции открывается реальное окно игры, которое Discord распознает для квеста.")

        active_id = self.spoofer.active_game.get("id") if (is_running and self.spoofer.active_game) else None
        for gid, card in self.cards.items():
            card.set_active(gid == active_id)

    def on_spoofer_tick(self, elapsed, total, percent, time_str):
        self.lbl_timer.setText(time_str)
        if self.spoofer.is_running:
            self.lbl_fps.setText(f"⚡ {random.randint(139, 145)} FPS")
            self.lbl_fps.show()
        w = int(self.progress_frame.width() * (percent / 100.0))
        self.progress_fill.setGeometry(0, 0, w, 10)

    def on_quest_completed(self, game_name):
        self.lbl_hud_status.setText(f"★ КВЕСТ ЗАВЕРШЕН: {game_name.upper()}! ЗАБЕРИТЕ НАГРАДУ В DISCORD ★")
        self.lbl_hud_status.setStyleSheet(f"color: {CYBER_GREEN};")
        # Ensure spoofer is stopped so timer does not tick or trigger again
        self.spoofer.stop()
        msg = QMessageBox(self)
        msg.setWindowTitle("ЗАДАНИЕ ВЫПОЛНЕНО!")
        msg.setText(
            f"15 минут игры в '{game_name}' успешно сымитированы!\n\n"
            f"Откройте Discord -> раздел Quests и заберите ваши Orbs / награду!"
        )
        msg.setIcon(QMessageBox.Information)
        msg.setStyleSheet(f"""
            QMessageBox {{ background-color: #0E1420; }}
            QLabel {{ color: #FFFFFF; font-family: Consolas; font-size: 13px; }}
            QPushButton {{
                background-color: {CYBER_YELLOW};
                color: #000000;
                font-family: Consolas;
                font-weight: bold;
                padding: 6px 16px;
                border-radius: 2px;
                min-width: 80px;
            }}
            QPushButton:hover {{ background-color: #FFFFFF; }}
        """)
        msg.exec_()

    def closeEvent(self, event):
        self.player.stop()
        self.spoofer.stop()
        event.accept()


class DiscordDatabaseUpdater(QThread):
    update_finished = pyqtSignal(bool, int, str)

    def __init__(self, target_path=None, parent=None):
        super().__init__(parent)
        self.target_path = target_path

    def run(self):
        url = "https://discord.com/api/v9/applications/detectable"
        try:
            import urllib.request
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req, timeout=15) as resp:
                data = json.loads(resp.read().decode('utf-8'))

            if not isinstance(data, list) or len(data) < 1000:
                self.update_finished.emit(False, 0, "Некорректный ответ от серверов Discord")
                return

            # Ensure Aniimo with aliases is included
            aniimo_entry = next((g for g in data if str(g.get('id')) == '1468082130474111047'), None)
            if aniimo_entry:
                aliases = aniimo_entry.setdefault('aliases', [])
                for a in ['ANIIMO GLOBAL LAUNCH', 'Aniimo Global Launch', 'Aniimo']:
                    if a not in aliases:
                        aliases.append(a)
            else:
                data.append({
                    'id': '1468082130474111047',
                    'name': 'Aniimo',
                    'aliases': ['ANIIMO GLOBAL LAUNCH', 'Aniimo Global Launch'],
                    'executables': [
                        {'is_launcher': False, 'name': 'aniimo.exe', 'os': 'win32'},
                        {'is_launcher': False, 'name': 'win64/aniimo.exe', 'os': 'win32'}
                    ]
                })

            # Ensure Forgotten Island is included
            if not any('forgotten island' in g.get('name', '').lower() for g in data):
                data.append({
                    'id': '1468199201984217088',
                    'name': 'Forgotten Island',
                    'aliases': ['FORGOTTEN ISLAND', 'The Forgotten Island'],
                    'executables': [
                        {'is_launcher': False, 'name': 'forgottenisland.exe', 'os': 'win32'},
                        {'is_launcher': False, 'name': 'win64/forgottenisland-win64-shipping.exe', 'os': 'win32'},
                        {'is_launcher': False, 'name': 'win64/forgottenisland.exe', 'os': 'win32'}
                    ]
                })

            if self.target_path:
                os.makedirs(os.path.dirname(os.path.abspath(self.target_path)), exist_ok=True)
                with open(self.target_path, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False)

            self.update_finished.emit(True, len(data), f"Успешно обновлено: {len(data)} игр!")
        except Exception as e:
            self.update_finished.emit(False, 0, f"Ошибка автообновления: {e}")


class AddGameDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("ДОБАВИТЬ НОВУЮ ИГРУ // DISCORD QUEST DATABASE")
        self.resize(600, 530)
        self.setStyleSheet(f"""
            QDialog {{
                background-color: #0E1420;
                border: 2px solid {CYBER_YELLOW};
            }}
            QLabel {{ color: #E2E8F0; font-family: Consolas; }}
            QLineEdit {{
                background-color: #0c121c;
                border: 1px solid {CYBER_CYAN};
                color: #FFFFFF;
                padding: 6px 10px;
                font-family: Consolas;
            }}
        """)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)
        layout.setSpacing(10)

        # Title bar with live update button
        title_row = QHBoxLayout()
        title = QLabel("➕ ПОИСК И ДОБАВЛЕНИЕ ИГРЫ (DISCORD ДЕТЕКТ)")
        title.setFont(QFont("Consolas", 11, QFont.Bold))
        title.setStyleSheet(f"color: {CYBER_YELLOW};")
        title_row.addWidget(title)
        title_row.addStretch()

        self.btn_update_db = QPushButton("🔄 ОБНОВИТЬ БАЗУ ОНЛАЙН")
        self.btn_update_db.setCursor(Qt.PointingHandCursor)
        self.btn_update_db.setStyleSheet(f"""
            QPushButton {{
                background-color: rgba(0, 240, 255, 20);
                border: 1px solid {CYBER_CYAN};
                color: {CYBER_CYAN};
                font-family: Consolas;
                font-size: 11px;
                font-weight: bold;
                padding: 4px 10px;
                border-radius: 2px;
            }}
            QPushButton:hover {{
                background-color: {CYBER_CYAN};
                color: #000000;
            }}
            QPushButton:disabled {{
                background-color: #1a2332;
                color: #64748b;
                border: 1px solid #334155;
            }}
        """)
        self.btn_update_db.clicked.connect(self.start_online_update)
        title_row.addWidget(self.btn_update_db)
        layout.addLayout(title_row)

        # Search / Game Title
        layout.addWidget(QLabel("Название игры (поиск по 24 300+ играм):"))
        self.in_name = QLineEdit()
        self.in_name.setPlaceholderText("например: Aniimo, Forgotten Island, Marvel Rivals, Cyberpunk...")
        self.in_name.textChanged.connect(self._on_name_search)
        layout.addWidget(self.in_name)

        # Suggestions list widget
        self.suggestions_list = QListWidget()
        self.suggestions_list.setFixedHeight(130)
        self.suggestions_list.setStyleSheet(f"""
            QListWidget {{
                background: #090D15;
                border: 1px solid {CYBER_CYAN};
                color: #FFFFFF;
                font-family: Consolas;
                font-size: 11px;
            }}
            QListWidget::item {{
                padding: 5px 8px;
                border-bottom: 1px solid rgba(0, 240, 255, 30);
            }}
            QListWidget::item:selected {{
                background: {CYBER_YELLOW};
                color: #000000;
                font-weight: bold;
            }}
            QListWidget::item:hover {{
                background: rgba(0, 240, 255, 60);
            }}
        """)
        self.suggestions_list.itemClicked.connect(self._on_suggestion_clicked)
        self.suggestions_list.hide()
        layout.addWidget(self.suggestions_list)

        # Detected Match Indicator
        self.lbl_detect_status = QLabel("ℹ База Discord: введите название для автоподбора")
        self.lbl_detect_status.setStyleSheet("color: #718096; font-size: 11px;")
        layout.addWidget(self.lbl_detect_status)

        # Executable input
        layout.addWidget(QLabel("Имя исполняемого файла игры (.exe):"))
        self.in_process = QLineEdit()
        self.in_process.setPlaceholderText("например: Game.exe")
        layout.addWidget(self.in_process)

        layout.addWidget(QLabel("Официальный Discord Client ID (авто-заполняется):"))
        self.in_client_id = QLineEdit()
        self.in_client_id.setPlaceholderText("например: 1468082130474111047")
        layout.addWidget(self.in_client_id)

        layout.addWidget(QLabel("Длительность квеста (минут):"))
        self.in_duration = QLineEdit("15")
        layout.addWidget(self.in_duration)

        btn_box = QHBoxLayout()
        self.btn_save = CyberGlitchButton("💾 СОХРАНИТЬ В БАЗУ", is_yellow=True)
        self.btn_save.clicked.connect(self.validate_and_save)

        self.btn_cancel = CyberGlitchButton("ОТМЕНА")
        self.btn_cancel.clicked.connect(self.reject)

        btn_box.addWidget(self.btn_save)
        btn_box.addWidget(self.btn_cancel)
        layout.addLayout(btn_box)

        self.game_data = None
        self._load_detectable_db()
        cnt = len(self.detectable_games) if self.detectable_games else 0
        self.lbl_detect_status.setText(f"ℹ База Discord ({cnt} игр): введите название для мгновенного поиска")

    def _get_writable_db_path(self):
        candidates = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "discord_detectable.json"),
            os.path.join(os.path.dirname(sys.executable), "discord_detectable.json")
        ]
        for c in candidates:
            try:
                if os.path.exists(c):
                    with open(c, "a"):
                        pass
                    return c
            except Exception:
                pass
        fallback = os.path.join(os.path.expanduser("~"), ".eshkeri", "discord_detectable.json")
        os.makedirs(os.path.dirname(fallback), exist_ok=True)
        return fallback

    def start_online_update(self):
        self.btn_update_db.setEnabled(False)
        self.btn_update_db.setText("⏳ Обновление...")
        self.lbl_detect_status.setText("🌐 Загрузка свежей базы игр с серверов Discord (24 300+ игр)...")
        self.lbl_detect_status.setStyleSheet(f"color: {CYBER_YELLOW}; font-size: 11px;")

        target_path = self._get_writable_db_path()
        self.updater_thread = DiscordDatabaseUpdater(target_path, self)
        self.updater_thread.update_finished.connect(self._on_update_finished)
        self.updater_thread.start()

    def _on_update_finished(self, success, count, message):
        self.btn_update_db.setEnabled(True)
        self.btn_update_db.setText("🔄 ОБНОВИТЬ БАЗУ ОНЛАЙН")
        if success:
            self._load_detectable_db()
            self.lbl_detect_status.setText(f"✔ База обновлена из Discord ({count} игр, включая ANIIMO и FORGOTTEN ISLAND)!")
            self.lbl_detect_status.setStyleSheet(f"color: {CYBER_GREEN}; font-size: 11px; font-weight: bold;")
            if self.in_name.text():
                self._on_name_search(self.in_name.text())
        else:
            self.lbl_detect_status.setText(f"⚠ {message}")
            self.lbl_detect_status.setStyleSheet(f"color: {CYBER_RED}; font-size: 11px;")

    def _load_detectable_db(self):
        self.detectable_games = []
        candidates = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "discord_detectable.json"),
            os.path.join(os.path.dirname(sys.executable), "discord_detectable.json"),
            os.path.join(getattr(sys, '_MEIPASS', ''), "discord_detectable.json"),
            os.path.join(os.path.expanduser("~"), ".eshkeri", "discord_detectable.json"),
        ]
        for c in candidates:
            if c and os.path.exists(c):
                try:
                    with open(c, "r", encoding="utf-8") as f:
                        self.detectable_games = json.load(f)
                    break
                except Exception as e:
                    print(f"Error loading detectable games: {e}")

    def _on_name_search(self, text):
        q = text.lower().strip()
        cnt = len(self.detectable_games) if self.detectable_games else 0
        if not q or not self.detectable_games:
            self.suggestions_list.hide()
            self.lbl_detect_status.setText(f"ℹ База Discord ({cnt} игр): введите название для автоподбора")
            self.lbl_detect_status.setStyleSheet("color: #718096; font-size: 11px;")
            return

        words = [w for w in q.split() if w]
        matches = []
        for g in self.detectable_games:
            name = g.get("name", "")
            aliases = g.get("aliases", [])
            corpus = (name + " " + " ".join(aliases)).lower()

            # Substring match or all words match
            if q in corpus:
                matches.append(g)
            elif all(w in corpus for w in words):
                matches.append(g)

            if len(matches) >= 30:
                break

        self.suggestions_list.clear()
        if matches:
            for g in matches:
                name = g.get("name", "")
                gid = str(g.get("id", ""))
                execs = [e.get("name") for e in g.get("executables", []) if e.get("os") == "win32"]
                # Prefer real game client executable over launchers
                best_exec = None
                for ex in execs:
                    ex_clean = ex.lower().replace("\\", "/")
                    if "shipping" in ex_clean or "win64" in ex_clean or "game" in ex_clean:
                        best_exec = ex
                        break
                if not best_exec:
                    for ex in execs:
                        ex_clean = ex.lower().replace("\\", "/")
                        if "launcher" not in ex_clean and "update" not in ex_clean and "crash" not in ex_clean:
                            best_exec = ex
                            break
                if not best_exec and execs:
                    best_exec = execs[0]

                pexe = best_exec.replace("\\", "/").split("/")[-1] if best_exec else f"{name.replace(' ', '')}.exe"
                path_rel = best_exec.replace("/", "\\") if best_exec else f"{name}\\{pexe}"

                item = QListWidgetItem(f"★ {name}  (ID: {gid} | exe: {pexe})")
                item.setData(Qt.UserRole, {
                    "name": name,
                    "id": gid,
                    "exe": pexe,
                    "path_rel": path_rel,
                    "all_execs": execs
                })
                self.suggestions_list.addItem(item)
            self.suggestions_list.show()
            self.lbl_detect_status.setText(f"✔ Найдено в базе Discord ({len(matches)} вариантов). Выберите из списка:")
            self.lbl_detect_status.setStyleSheet(f"color: {CYBER_CYAN}; font-size: 11px; font-weight: bold;")
        else:
            self.suggestions_list.hide()
            self.lbl_detect_status.setText("⚡ Ручной режим: игра запустится в окне для системного детекта Discord")
            self.lbl_detect_status.setStyleSheet(f"color: {CYBER_CYAN}; font-size: 11px;")

    def _on_suggestion_clicked(self, item):
        data = item.data(Qt.UserRole)
        if data:
            self.in_name.blockSignals(True)
            self.in_name.setText(data["name"])
            self.in_name.blockSignals(False)
            self.in_process.setText(data["exe"])
            self.in_client_id.setText(data["id"])
            self.selected_path_rel = data.get("path_rel")
            self.selected_all_execs = data.get("all_execs", [])
            self.suggestions_list.hide()
            self.lbl_detect_status.setText(f"✔ Выбрана игра: {data['name']} (ID: {data['id']})")
            self.lbl_detect_status.setStyleSheet(f"color: {CYBER_GREEN}; font-size: 11px; font-weight: bold;")

    def validate_and_save(self):
        name = self.in_name.text().strip()
        proc = self.in_process.text().strip()
        cid = self.in_client_id.text().strip()
        dur = self.in_duration.text().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Название игры обязательно!")
            return

        if not proc:
            proc = f"{name.replace(' ', '')}.exe"

        if not proc.lower().endswith(".exe"):
            proc += ".exe"

        # If client_id is not filled, try automatic lookup from detectable db
        if not cid and self.detectable_games:
            for g in self.detectable_games:
                if g.get("name", "").lower() == name.lower():
                    cid = str(g.get("id", ""))
                    break

        try:
            dur_int = int(dur)
        except ValueError:
            dur_int = 15

        path_rel = getattr(self, 'selected_path_rel', None) or f"{name}/{proc}"
        extra_execs = getattr(self, 'selected_all_execs', [])

        self.game_data = {
            "id": "custom_" + str(abs(hash(name)))[:8],
            "name": name,
            "client_id": cid if cid else None,
            "process": proc,
            "path_rel": path_rel,
            "window_title": name,
            "category": "Custom / Quest",
            "duration_minutes": dur_int,
            "description": f"Discord Quest для {name}",
            "accent_color": "#00F0FF",
            "extra_executables": [e for e in extra_execs if e != path_rel]
        }
        self.accept()
