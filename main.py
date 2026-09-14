import os
import sys
import traceback

os.environ["QT_MULTIMEDIA_PREFERRED_PLUGINS"] = "windowsmediafoundation"

def main():
    # Determine base directory (PyInstaller _MEIPASS or script dir)
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

    # Setup crash log file next to the executable (not inside _MEIPASS temp)
    if getattr(sys, 'frozen', False):
        exe_dir = os.path.dirname(sys.executable)
    else:
        exe_dir = os.path.dirname(os.path.abspath(__file__))
    crash_log = os.path.join(exe_dir, "eshkeri_crash.log")

    try:
        from PyQt5.QtCore import Qt, QCoreApplication, QTimer
        from PyQt5.QtWidgets import QApplication
        from PyQt5.QtGui import QIcon

        # Enable High DPI scaling
        QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
        QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

        app = QApplication(sys.argv)
        app.setApplicationName("Eshkeri")
        app.setOrganizationName("Eshkeri")

        icon_png = os.path.join(base_dir, "app_icon.png")
        icon_ico = os.path.join(base_dir, "app_icon.ico")

        if os.path.exists(icon_ico):
            app.setWindowIcon(QIcon(icon_ico))
        elif os.path.exists(icon_png):
            app.setWindowIcon(QIcon(icon_png))

        from spoofer import SpooferEngine
        from glitch_intro import GlitchIntroWidget
        from main_window import MainWindow

        # Initialize backend engine
        spoofer_engine = SpooferEngine()

        # Main window (hidden initially)
        main_win = MainWindow(spoofer_engine, icon_path=icon_png)

        # Launch Glitch Intro Widget
        intro = GlitchIntroWidget(icon_path=icon_png)

        intro_finished = [False]
        def on_intro_done():
            if not intro_finished[0]:
                intro_finished[0] = True
                try:
                    intro.timer.stop()
                except Exception:
                    pass
                intro.close()
                main_win.show()
                main_win.raise_()
                main_win.activateWindow()

        intro.finished.connect(on_intro_done)
        intro.show()
        intro.raise_()
        intro.activateWindow()

        # Fallback timer: guarantee main_win shows after at most 4 seconds
        QTimer.singleShot(4000, on_intro_done)

        sys.exit(app.exec_())

    except Exception as e:
        error_msg = traceback.format_exc()
        try:
            with open(crash_log, "w", encoding="utf-8") as f:
                f.write(f"ESHKERI CRASH LOG\n{'='*50}\n")
                f.write(f"Python: {sys.version}\n")
                f.write(f"Frozen: {getattr(sys, 'frozen', False)}\n")
                f.write(f"MEIPASS: {getattr(sys, '_MEIPASS', 'N/A')}\n")
                f.write(f"base_dir: {base_dir}\n")
                f.write(f"exe_dir: {exe_dir}\n")
                f.write(f"{'='*50}\n")
                f.write(error_msg)
        except Exception:
            pass
        raise

if __name__ == "__main__":
    main()
