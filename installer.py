import os
import sys
import time
import zipfile
import subprocess
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QPoint, QRect
from PyQt5.QtGui import QFont, QColor, QPainter, QIcon, QPixmap, QPen
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QLineEdit, QFileDialog, QProgressBar, QCheckBox,
    QFrame, QMessageBox
)

CYBER_YELLOW = "#FCEE0A"
CYBER_CYAN   = "#00F0FF"
CYBER_RED    = "#FF003C"
CYBER_GREEN  = "#00FF66"

class CyberButton(QPushButton):
    def __init__(self, text="", parent=None, is_yellow=True, is_red=False):
        super().__init__(text, parent)
        self.is_yellow = is_yellow
        self.is_red = is_red
        self.setCursor(Qt.PointingHandCursor)
        self._update_style()

    def _update_style(self):
        if self.is_yellow:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: {CYBER_YELLOW};
                    border: 2px solid {CYBER_YELLOW};
                    color: #000000;
                    font-family: 'Segoe UI', Consolas, sans-serif;
                    font-weight: bold;
                    font-size: 13px;
                    padding: 9px 18px;
                    border-radius: 2px;
                }}
                QPushButton:hover {{
                    background-color: #FFFFFF;
                    border: 2px solid {CYBER_CYAN};
                    color: #000000;
                }}
                QPushButton:disabled {{
                    background-color: #4A4D10;
                    color: #888888;
                    border: 2px solid #555555;
                }}
            """)
        elif self.is_red:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: rgba(56, 12, 20, 200);
                    border: 1px solid {CYBER_RED};
                    color: {CYBER_RED};
                    font-family: Consolas, sans-serif;
                    font-weight: bold;
                    font-size: 13px;
                    padding: 9px 18px;
                    border-radius: 2px;
                }}
                QPushButton:hover {{
                    background-color: {CYBER_RED};
                    color: #FFFFFF;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background-color: #101622;
                    border: 1px solid {CYBER_CYAN};
                    color: {CYBER_CYAN};
                    font-family: Consolas, sans-serif;
                    font-weight: bold;
                    font-size: 13px;
                    padding: 9px 18px;
                    border-radius: 2px;
                }}
                QPushButton:hover {{
                    background-color: {CYBER_CYAN};
                    color: #000000;
                }}
            """)


class InstallThread(QThread):
    progress = pyqtSignal(int, str)
    finished_signal = pyqtSignal(bool, str)

    def __init__(self, payload_path, target_dir, create_desktop, create_start_menu):
        super().__init__()
        self.payload_path = payload_path
        self.target_dir = target_dir
        self.create_desktop = create_desktop
        self.create_start_menu = create_start_menu

    def run(self):
        try:
            if not os.path.exists(self.payload_path):
                self.finished_signal.emit(False, f"Архив пакета не найден: {self.payload_path}")
                return

            os.makedirs(self.target_dir, exist_ok=True)

            with zipfile.ZipFile(self.payload_path, "r") as zf:
                file_list = zf.namelist()
                total = len(file_list)

                for i, name in enumerate(file_list):
                    pct = int(((i + 1) / float(total)) * 85)
                    self.progress.emit(pct, f"Распаковка: {name}")
                    zf.extract(name, self.target_dir)
                    time.sleep(0.015)

            target_exe = os.path.join(self.target_dir, "Eshkeri.exe")
            icon_file = os.path.join(self.target_dir, "app_icon.ico")

            # Shortcuts
            self.progress.emit(90, "Создание ярлыков Windows...")

            if self.create_desktop:
                desktop_dir = os.path.join(os.environ.get("USERPROFILE", os.path.expanduser("~")), "Desktop")
                if os.path.exists(desktop_dir):
                    lnk_path = os.path.join(desktop_dir, "Eshkeri.lnk")
                    self._create_shortcut(target_exe, lnk_path, self.target_dir, icon_file)

            if self.create_start_menu:
                appdata = os.environ.get("APPDATA", "")
                if appdata:
                    start_dir = os.path.join(appdata, "Microsoft", "Windows", "Start Menu", "Programs")
                    if os.path.exists(start_dir):
                        lnk_path = os.path.join(start_dir, "Eshkeri.lnk")
                        self._create_shortcut(target_exe, lnk_path, self.target_dir, icon_file)

            self.progress.emit(100, "Установка успешно завершена!")
            self.finished_signal.emit(True, "Установка выполнена успешно!")
        except Exception as e:
            self.finished_signal.emit(False, str(e))

    def _create_shortcut(self, target_exe, lnk_path, work_dir, icon_path):
        try:
            icon_loc = f"{icon_path},0" if (icon_path and os.path.exists(icon_path)) else f"{target_exe},0"
            ps_cmd = (
                f'$ws = New-Object -ComObject WScript.Shell; '
                f'$s = $ws.CreateShortcut("{lnk_path}"); '
                f'$s.TargetPath = "{target_exe}"; '
                f'$s.WorkingDirectory = "{work_dir}"; '
                f'$s.IconLocation = "{icon_loc}"; '
                f'$s.Save()'
            )
            subprocess.run(
                ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", ps_cmd],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                creationflags=subprocess.CREATE_NO_WINDOW if hasattr(subprocess, "CREATE_NO_WINDOW") else 0
            )
        except Exception:
            pass


class InstallerWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.drag_position = QPoint()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.resize(720, 540)
        self.setMinimumSize(700, 500)
        self.setStyleSheet("background-color: #090C12; color: #FFFFFF; font-family: Consolas, sans-serif;")

        # Locate payload.zip
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        self.payload_path = os.path.join(base_dir, "payload.zip")
        if not os.path.exists(self.payload_path):
            self.payload_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "payload.zip")
        if not os.path.exists(self.payload_path):
            self.payload_path = os.path.join(os.path.dirname(sys.executable), "payload.zip")

        # Set Icon
        icon_path = os.path.join(base_dir, "app_icon.ico")
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))

        self.init_ui()

    def init_ui(self):
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(18, 14, 18, 18)
        main_layout.setSpacing(12)

        # 1. Custom Title Bar
        title_bar = QHBoxLayout()
        lbl_app = QLabel("⚡ ESHKERI SETUP")
        lbl_app.setFont(QFont("Impact", 16))
        lbl_app.setStyleSheet(f"color: {CYBER_YELLOW}; letter-spacing: 1px;")
        title_bar.addWidget(lbl_app)

        lbl_ver = QLabel("// МАСТЕР УСТАНОВКИ 2077")
        lbl_ver.setFont(QFont("Consolas", 10, QFont.Bold))
        lbl_ver.setStyleSheet(f"color: {CYBER_CYAN};")
        title_bar.addWidget(lbl_ver)

        title_bar.addStretch()

        btn_min = QPushButton("—")
        btn_min.setFixedSize(30, 26)
        btn_min.setStyleSheet("color: #FFFFFF; background: transparent; border: none; font-size: 14px; font-weight: bold;")
        btn_min.clicked.connect(self.showMinimized)
        title_bar.addWidget(btn_min)

        btn_close = QPushButton("✕")
        btn_close.setFixedSize(30, 26)
        btn_close.setStyleSheet("color: #FF003C; background: transparent; border: none; font-size: 15px; font-weight: bold;")
        btn_close.clicked.connect(self.close)
        title_bar.addWidget(btn_close)

        main_layout.addLayout(title_bar)

        # 2. Hero Info Banner
        banner_frame = QFrame()
        banner_frame.setStyleSheet("background: rgba(14, 20, 32, 230); border: 1px solid rgba(0, 240, 255, 100); border-radius: 4px;")
        banner_layout = QHBoxLayout(banner_frame)
        banner_layout.setContentsMargins(16, 14, 16, 14)
        banner_layout.setSpacing(16)

        lbl_logo = QLabel("⚡")
        lbl_logo.setFont(QFont("Impact", 36))
        lbl_logo.setStyleSheet(f"color: {CYBER_YELLOW};")
        banner_layout.addWidget(lbl_logo)

        desc_layout = QVBoxLayout()
        desc_layout.setSpacing(4)
        lbl_title = QLabel("УСТАНОВКА ПРОГРАММЫ И ПОЛНОГО ИСХОДНОГО КОДА")
        lbl_title.setFont(QFont("Impact", 14))
        lbl_title.setStyleSheet(f"color: {CYBER_YELLOW};")
        desc_layout.addWidget(lbl_title)

        lbl_sub = QLabel(
            "Будет установлена готовая программа Eshkeri.exe (Discord Quests Spoofer),\n"
            "фоновое видео fonpril.mp4, документация README.txt, а также полный исходный\n"
            "код приложения со всеми модулями и папками (main.py, main_window.py, icons/ и др.)."
        )
        lbl_sub.setStyleSheet("color: #CBD5E1; font-size: 11px; line-height: 1.4;")
        desc_layout.addWidget(lbl_sub)
        banner_layout.addLayout(desc_layout, stretch=1)
        main_layout.addWidget(banner_frame)

        # 3. Path Selection Frame
        self.path_frame = QFrame()
        self.path_frame.setStyleSheet("background: rgba(14, 20, 32, 230); border: 1px solid #202D42; border-radius: 4px;")
        path_layout = QVBoxLayout(self.path_frame)
        path_layout.setContentsMargins(16, 12, 16, 14)
        path_layout.setSpacing(10)

        lbl_choose = QLabel("Папка для установки программы и исходников:")
        lbl_choose.setFont(QFont("Consolas", 10, QFont.Bold))
        lbl_choose.setStyleSheet(f"color: {CYBER_CYAN};")
        path_layout.addWidget(lbl_choose)

        dir_h = QHBoxLayout()
        default_dir = os.path.join(os.environ.get("LOCALAPPDATA", os.path.expanduser("~")), "Programs", "Eshkeri")
        self.in_dir = QLineEdit(default_dir)
        self.in_dir.setStyleSheet(f"""
            QLineEdit {{
                background: #0B101A;
                border: 1px solid {CYBER_CYAN};
                color: #FFFFFF;
                padding: 7px 12px;
                font-family: Consolas;
                font-size: 12px;
            }}
        """)
        dir_h.addWidget(self.in_dir, stretch=1)

        btn_browse = CyberButton("📂 Обзор...", is_yellow=False)
        btn_browse.clicked.connect(self.browse_dir)
        dir_h.addWidget(btn_browse)
        path_layout.addLayout(dir_h)

        # Options Checkboxes
        opt_layout = QHBoxLayout()
        self.cb_desktop = QCheckBox("Создать ярлык на Рабочем столе")
        self.cb_desktop.setChecked(True)
        self.cb_desktop.setStyleSheet(f"QCheckBox {{ color: #E2E8F0; font-size: 12px; }} QCheckBox::indicator:checked {{ background-color: {CYBER_YELLOW}; border: 1px solid {CYBER_YELLOW}; }}")
        opt_layout.addWidget(self.cb_desktop)

        self.cb_start = QCheckBox("Создать ярлык в меню «Пуск»")
        self.cb_start.setChecked(True)
        self.cb_start.setStyleSheet(f"QCheckBox {{ color: #E2E8F0; font-size: 12px; }} QCheckBox::indicator:checked {{ background-color: {CYBER_YELLOW}; border: 1px solid {CYBER_YELLOW}; }}")
        opt_layout.addWidget(self.cb_start)
        opt_layout.addStretch()
        path_layout.addLayout(opt_layout)

        main_layout.addWidget(self.path_frame)

        # 4. Progress & Status Frame
        self.progress_frame = QFrame()
        self.progress_frame.setStyleSheet("background: rgba(14, 20, 32, 230); border: 1px solid #202D42; border-radius: 4px;")
        prog_layout = QVBoxLayout(self.progress_frame)
        prog_layout.setContentsMargins(16, 12, 16, 12)
        prog_layout.setSpacing(8)

        self.lbl_status = QLabel("Готов к установке. Нажмите кнопку ниже для запуска.")
        self.lbl_status.setFont(QFont("Consolas", 11))
        self.lbl_status.setStyleSheet("color: #CBD5E1;")
        prog_layout.addWidget(self.lbl_status)

        self.pbar = QProgressBar()
        self.pbar.setFixedHeight(18)
        self.pbar.setRange(0, 100)
        self.pbar.setValue(0)
        self.pbar.setTextVisible(False)
        self.pbar.setStyleSheet(f"""
            QProgressBar {{
                background: #090E17;
                border: 1px solid rgba(0, 240, 255, 100);
                border-radius: 2px;
            }}
            QProgressBar::chunk {{
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 {CYBER_CYAN}, stop:1 {CYBER_YELLOW});
                border-radius: 2px;
            }}
        """)
        prog_layout.addWidget(self.pbar)
        main_layout.addWidget(self.progress_frame)

        # 5. Bottom Action Controls
        self.bottom_layout = QHBoxLayout()
        self.cb_launch = QCheckBox("Запустить Eshkeri после завершения")
        self.cb_launch.setChecked(True)
        self.cb_launch.setStyleSheet(f"QCheckBox {{ color: {CYBER_GREEN}; font-weight: bold; font-size: 12px; }} QCheckBox::indicator:checked {{ background-color: {CYBER_GREEN}; border: 1px solid {CYBER_GREEN}; }}")
        self.cb_launch.hide()
        self.bottom_layout.addWidget(self.cb_launch)

        self.btn_open_folder = CyberButton("📂 Открыть папку", is_yellow=False)
        self.btn_open_folder.clicked.connect(self.open_installed_folder)
        self.btn_open_folder.hide()
        self.bottom_layout.addWidget(self.btn_open_folder)

        self.bottom_layout.addStretch()

        self.btn_action = CyberButton("⚡ НАЧАТЬ УСТАНОВКУ", is_yellow=True)
        self.btn_action.clicked.connect(self.start_installation)
        self.bottom_layout.addWidget(self.btn_action)

        self.btn_cancel = CyberButton("ОТМЕНА", is_yellow=False, is_red=True)
        self.btn_cancel.clicked.connect(self.close)
        self.bottom_layout.addWidget(self.btn_cancel)

        main_layout.addLayout(self.bottom_layout)

    def browse_dir(self):
        d = QFileDialog.getExistingDirectory(self, "Выберите папку для установки", self.in_dir.text())
        if d:
            self.in_dir.setText(os.path.join(d, "Eshkeri") if not d.lower().endswith("eshkeri") else d)

    def start_installation(self):
        target = self.in_dir.text().strip()
        if not target:
            QMessageBox.warning(self, "Ошибка", "Укажите папку для установки!")
            return

        self.target_dir = target
        self.btn_action.setEnabled(False)
        self.btn_cancel.setEnabled(False)
        self.in_dir.setEnabled(False)
        self.cb_desktop.setEnabled(False)
        self.cb_start.setEnabled(False)

        self.lbl_status.setText("Инициализация пакета установки...")
        self.lbl_status.setStyleSheet(f"color: {CYBER_YELLOW};")

        self.thread = InstallThread(
            self.payload_path,
            target,
            self.cb_desktop.isChecked(),
            self.cb_start.isChecked()
        )
        self.thread.progress.connect(self.on_progress)
        self.thread.finished_signal.connect(self.on_finished)
        self.thread.start()

    def on_progress(self, val, msg):
        self.pbar.setValue(val)
        self.lbl_status.setText(msg)

    def on_finished(self, success, msg):
        self.btn_cancel.hide()
        if success:
            self.lbl_status.setText(f"★ УСТАНОВКА УСПЕШНО ЗАВЕРШЕНА! ★\nВсе файлы и исходный код сохранены в: {self.target_dir}")
            self.lbl_status.setStyleSheet(f"color: {CYBER_GREEN}; font-weight: bold;")
            self.btn_open_folder.show()
            self.cb_launch.show()
            self.btn_action.setText("ЗАВЕРШИТЬ")
            self.btn_action.setEnabled(True)
            self.btn_action.clicked.disconnect()
            self.btn_action.clicked.connect(self.finish_install)
        else:
            self.lbl_status.setText(f"Ошибка при установке: {msg}")
            self.lbl_status.setStyleSheet(f"color: {CYBER_RED}; font-weight: bold;")
            self.btn_action.setText("ЗАКРЫТЬ")
            self.btn_action.setEnabled(True)
            self.btn_action.clicked.disconnect()
            self.btn_action.clicked.connect(self.close)

    def open_installed_folder(self):
        if hasattr(self, 'target_dir') and os.path.exists(self.target_dir):
            os.startfile(self.target_dir)

    def finish_install(self):
        if self.cb_launch.isChecked():
            exe_path = os.path.join(self.target_dir, "Eshkeri.exe")
            if os.path.exists(exe_path):
                subprocess.Popen([exe_path], cwd=self.target_dir)
        self.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and event.pos().y() < 50:
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

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        w, h = self.width(), self.height()
        pen = QPen(QColor(CYBER_YELLOW), 2)
        painter.setPen(pen)
        painter.drawRect(1, 1, w - 2, h - 2)
        painter.end()


def main():
    app = QApplication(sys.argv)
    win = InstallerWindow()
    win.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
