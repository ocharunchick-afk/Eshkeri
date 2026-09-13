import os
import sys
import random
from PyQt5.QtCore import Qt, QTimer, QRect, QRectF, pyqtSignal
from PyQt5.QtGui import (
    QPainter, QColor, QFont, QPixmap, QImage, QPainterPath,
    QLinearGradient, QPen, QBrush
)
from PyQt5.QtWidgets import QWidget

class GlitchIntroWidget(QWidget):
    finished = pyqtSignal()

    def __init__(self, icon_path=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eshkeri Intro")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, False)
        self.resize(750, 480)

        # Center on screen
        from PyQt5.QtWidgets import QApplication
        screen = QApplication.primaryScreen().geometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2
        )

        # Load avatar / icon
        if icon_path and os.path.exists(icon_path):
            self.base_pixmap = QPixmap(icon_path).scaled(160, 160, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        else:
            self.base_pixmap = None

        self.frame_count = 0
        self.max_frames = 150  # ~2.5 seconds at 60 FPS
        self.glitch_slices = []
        self.rgb_split_offset = 0
        self.terminal_lines = [
            ">> INITIALIZING SANDEVISTAN BIOS 2.077...",
            ">> NEURAL INTERFACE: CONNECTED",
            ">> DISCORD IPC HANDSHAKE... ACTIVE",
            ">> ORBS HARVEST ENGINE: INITIALIZED",
            ">> PROTOCOL: ESHKERI OVERDRIVE READY!"
        ]
        self.displayed_text = ""

        # 60 FPS Timer (16ms)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self._update_animation)
        self.timer.start(16)

    def _update_animation(self):
        self.frame_count += 1

        # Text typing effect
        line_idx = min(len(self.terminal_lines) - 1, self.frame_count // 25)
        chars = min(len(self.terminal_lines[line_idx]), (self.frame_count % 25) * 3)
        self.displayed_text = "\n".join(self.terminal_lines[:line_idx]) + "\n" + self.terminal_lines[line_idx][:chars]

        # Glitch parameters
        if random.random() < 0.35:
            # Active glitch burst
            self.rgb_split_offset = random.choice([-8, -5, 5, 8, 12, -12])
            num_slices = random.randint(2, 6)
            self.glitch_slices = [
                (random.randint(40, self.height() - 60), random.randint(10, 45), random.randint(-25, 25))
                for _ in range(num_slices)
            ]
        else:
            self.rgb_split_offset = 0
            self.glitch_slices = []

        self.update()

        if self.frame_count >= self.max_frames:
            self.timer.stop()
            self.finished.emit()

    def mousePressEvent(self, event):
        # Allow skipping intro by click
        self.timer.stop()
        self.finished.emit()

    def keyPressEvent(self, event):
        # Allow skipping intro by key
        self.timer.stop()
        self.finished.emit()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.setRenderHint(QPainter.TextAntialiasing, True)

        w, h = self.width(), self.height()

        # 1. Dark Tech Cyberpunk Background
        bg_gradient = QLinearGradient(0, 0, w, h)
        bg_gradient.setColorAt(0.0, QColor("#08090E"))
        bg_gradient.setColorAt(0.6, QColor("#0D111A"))
        bg_gradient.setColorAt(1.0, QColor("#05070B"))
        painter.fillRect(self.rect(), bg_gradient)

        # 2. Cyber Grid Lines
        pen_grid = QPen(QColor(0, 240, 255, 18), 1)
        painter.setPen(pen_grid)
        for x in range(0, w, 32):
            painter.drawLine(x, 0, x, h)
        for y in range(0, h, 32):
            painter.drawLine(0, y, w, y)

        # 3. Scanlines effect
        painter.setPen(QColor(0, 0, 0, 60))
        for y in range(0, h, 4):
            painter.drawLine(0, y, w, y)

        # 4. Cyberpunk Yellow Outer Border with angled corners
        pen_border = QPen(QColor("#FCEE0A"), 2)
        painter.setPen(pen_border)
        # Top-left cut, bottom-right cut
        path = QPainterPath()
        path.moveTo(30, 2)
        path.lineTo(w - 2, 2)
        path.lineTo(w - 2, h - 30)
        path.lineTo(w - 30, h - 2)
        path.lineTo(2, h - 2)
        path.lineTo(2, 30)
        path.closeSubpath()
        painter.drawPath(path)

        # Neon corner accents
        painter.setPen(QPen(QColor("#00F0FF"), 3))
        # Top-left bracket
        painter.drawLine(10, 10, 40, 10)
        painter.drawLine(10, 10, 10, 40)
        # Top-right bracket
        painter.drawLine(w - 40, 10, w - 10, 10)
        painter.drawLine(w - 10, 10, w - 10, 40)
        # Bottom-left bracket
        painter.drawLine(10, h - 40, 10, h - 10)
        painter.drawLine(10, h - 10, 40, h - 10)
        # Bottom-right bracket
        painter.drawLine(w - 40, h - 10, w - 10, h - 10)
        painter.drawLine(w - 10, h - 40, w - 10, h - 10)

        # 5. Draw Avatar with Glitch / Chromatic split
        if self.base_pixmap:
            cx = w // 2 - 80
            cy = 70

            # Yellow frame around avatar
            frame_rect = QRect(cx - 6, cy - 6, 172, 172)
            painter.setPen(QPen(QColor("#FCEE0A"), 2))
            painter.setBrush(QColor(20, 20, 30, 200))
            painter.drawRect(frame_rect)

            # Chromatic RGB shift when glitching
            if self.rgb_split_offset != 0:
                # Cyan ghost
                painter.setOpacity(0.55)
                painter.drawPixmap(cx + self.rgb_split_offset, cy, self.base_pixmap)
                # Red ghost
                painter.setOpacity(0.55)
                painter.drawPixmap(cx - self.rgb_split_offset, cy, self.base_pixmap)
                painter.setOpacity(1.0)
            
            # Base avatar
            painter.drawPixmap(cx, cy, self.base_pixmap)

            # Glitch slices across avatar
            for sy, sh, sx in self.glitch_slices:
                if cy <= sy <= cy + 160:
                    slice_rect = QRect(cx + sx, sy, 160, min(sh, cy + 160 - sy))
                    painter.fillRect(slice_rect, QColor(0, 240, 255, 60))

        # 6. Title: ESHKERI
        painter.setOpacity(1.0)
        font_title = QFont("Impact", 36, QFont.Bold)
        font_title.setLetterSpacing(QFont.AbsoluteSpacing, 6)
        painter.setFont(font_title)

        title_text = "ESHKE•RI"
        # Chromatic glitch for title text
        if self.rgb_split_offset != 0:
            painter.setPen(QColor("#FF003C"))
            painter.drawText(QRect(self.rgb_split_offset, 250, w, 50), Qt.AlignCenter, title_text)
            painter.setPen(QColor("#00F0FF"))
            painter.drawText(QRect(-self.rgb_split_offset, 250, w, 50), Qt.AlignCenter, title_text)

        painter.setPen(QColor("#FCEE0A"))
        painter.drawText(QRect(0, 250, w, 50), Qt.AlignCenter, title_text)

        # 7. Subtitle / Badge
        font_sub = QFont("Consolas", 11, QFont.Bold)
        font_sub.setLetterSpacing(QFont.AbsoluteSpacing, 3)
        painter.setFont(font_sub)
        painter.setPen(QColor("#00F0FF"))
        painter.drawText(QRect(0, 305, w, 25), Qt.AlignCenter, "EDGERUNNERS // DISCORD QUESTS ORBS PROTOCOL")

        # 8. Terminal Log Lines (Cyberpunk typing)
        font_term = QFont("Consolas", 9)
        painter.setFont(font_term)
        painter.setPen(QColor("#80FF90"))
        log_rect = QRect(60, 340, w - 120, 100)
        painter.drawText(log_rect, Qt.AlignLeft | Qt.AlignTop, self.displayed_text)

        # 9. Loading progress bar at bottom
        bar_w = w - 120
        progress_ratio = min(1.0, self.frame_count / float(self.max_frames))
        bar_x = 60
        bar_y = h - 35

        # Background track
        painter.setPen(Qt.NoPen)
        painter.setBrush(QColor(255, 255, 255, 20))
        painter.drawRect(bar_x, bar_y, bar_w, 6)

        # Neon Yellow / Cyan Fill
        fill_grad = QLinearGradient(bar_x, bar_y, bar_x + bar_w, bar_y)
        fill_grad.setColorAt(0.0, QColor("#00F0FF"))
        fill_grad.setColorAt(1.0, QColor("#FCEE0A"))
        painter.setBrush(fill_grad)
        painter.drawRect(bar_x, bar_y, int(bar_w * progress_ratio), 6)

        # Skip prompt
        font_skip = QFont("Consolas", 8)
        painter.setFont(font_skip)
        painter.setPen(QColor(150, 150, 150, 160))
        painter.drawText(QRect(0, h - 25, w - 60, 20), Qt.AlignRight, "CLICK OR PRESS ANY KEY TO SKIP >>")
