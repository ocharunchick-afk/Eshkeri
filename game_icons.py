import os
import sys
from PyQt5.QtCore import Qt, QRect, QRectF
from PyQt5.QtGui import (
    QPainter, QColor, QFont, QPixmap, QPainterPath,
    QPen, QBrush
)

def create_cyber_game_icon(game_id, size=64):
    """Returns the official game icon with a cyberpunk styled frame"""
    base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    icon_path = os.path.join(base_dir, "icons", f"{game_id}.png")

    out_pix = QPixmap(size, size)
    out_pix.fill(Qt.transparent)

    painter = QPainter(out_pix)
    painter.setRenderHint(QPainter.Antialiasing, True)
    painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

    accent_colors = {
        "cyberpunk2077": QColor("#FCEE0A"),
        "endfield": QColor("#00F0FF"),
        "pragmata": QColor("#FFB300"),
        "re_requiem": QColor("#FF003C"),
        "wwm": QColor("#00F0FF"),
        "genshin": QColor("#00F0FF"),
        "hsr": QColor("#D070FF"),
        "roblox": QColor("#00A2FF"),
        "forest3": QColor("#FF003C")
    }
    accent = accent_colors.get(game_id, QColor("#00F0FF"))

    # Cut-corner cyberpunk rounded container
    clip_path = QPainterPath()
    clip_path.addRoundedRect(1, 1, size - 2, size - 2, 8, 8)

    if os.path.exists(icon_path):
        src_pix = QPixmap(icon_path)
        if not src_pix.isNull():
            painter.setClipPath(clip_path)
            # Draw original game icon scaled to fit
            painter.drawPixmap(0, 0, size, size, src_pix.scaled(size, size, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
            painter.setClipping(False)

            # Neon glowing border
            painter.setPen(QPen(accent, 2))
            painter.drawRoundedRect(1, 1, size - 2, size - 2, 8, 8)
            painter.end()
            return out_pix

    # Fallback if image not found
    painter.fillPath(clip_path, QColor(14, 20, 32, 230))
    painter.setPen(QPen(accent, 2))
    painter.drawPath(clip_path)
    painter.setFont(QFont("Impact", 10))
    painter.setPen(accent)
    painter.drawText(QRect(0, 0, size, size), Qt.AlignCenter, game_id[:4].upper())
    painter.end()
    return out_pix
