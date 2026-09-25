# ==============================================================================
#                  ⚡ ESHKERI // ANDROID APK BUILDER & ENGINE v2.7 ⚡
#   100% Standalone Mobile Discord Quests (NO PC NEEDED, Auto-Enroll & Heartbeats),
#   Live @me Quests Sync, Background Video (fonpril.mp4), PC-like Game Add/Search
# ==============================================================================

import os
import sys
import io
import json
import zipfile
import subprocess
from PIL import Image, ImageDraw

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(BASE_DIR, "Android_App")
OUTPUT_APK = os.path.join(OUTPUT_DIR, "Eshkeri.apk")
ROOT_APK = os.path.join(BASE_DIR, "Eshkeri.apk")
DESKTOP_DIR = os.path.expanduser(r"~\OneDrive\Desktop\esheri protokol")
DESKTOP_APK = os.path.join(DESKTOP_DIR, "Eshkeri.apk") if os.path.exists(DESKTOP_DIR) else None
TEMPLATE_APK = os.path.join(BASE_DIR, "temp_app.apk")
SIGNER_JAR = os.path.join(BASE_DIR, "uber-apk-signer.jar")
DETECTABLE_SRC = os.path.join(BASE_DIR, "discord_detectable.json")
FONPRIL_PATH = os.path.join(BASE_DIR, "fonpril.mp4")

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>Eshkeri // Standalone Mobile Discord Quest Spoofer</title>
<style>
:root {
  --bg: #070B14;
  --panel: rgba(14, 22, 38, 0.94);
  --card: rgba(19, 30, 51, 0.94);
  --cyan: #00F0FF;
  --yellow: #FCEE0A;
  --red: #FF003C;
  --green: #00FF66;
  --purple: #A855F7;
  --text: #F1F5F9;
  --subtext: #94A3B8;
  --border: rgba(0, 240, 255, 0.28);
}

* { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; -webkit-tap-highlight-color: rgba(0, 240, 255, 0.2); }
body { background: var(--bg); color: var(--text); min-height: 100vh; overflow-x: hidden; padding-bottom: 70px; position: relative; }

/* Background Cyberpunk Video */
#bgVideo {
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  object-fit: cover;
  z-index: -2;
  opacity: 0.38;
  pointer-events: none;
}
.bg-overlay {
  position: fixed;
  top: 0; left: 0; width: 100vw; height: 100vh;
  background: radial-gradient(circle at center, rgba(7, 11, 20, 0.55) 0%, rgba(7, 11, 20, 0.94) 100%);
  z-index: -1;
  pointer-events: none;
}

/* Header */
header {
  padding: 12px 16px;
  background: rgba(10, 15, 26, 0.96);
  border-bottom: 2px solid var(--cyan);
  box-shadow: 0 4px 25px rgba(0, 240, 255, 0.25);
  display: flex; align-items: center; justify-content: space-between;
  backdrop-filter: blur(8px);
}
.logo-title { font-size: 16px; font-weight: 900; letter-spacing: 2px; color: var(--yellow); text-shadow: 0 0 10px rgba(252, 238, 10, 0.6); }
.logo-sub { font-size: 9px; color: var(--cyan); letter-spacing: 1px; }
.header-actions { display: flex; align-items: center; gap: 8px; }
.status-badge {
  font-size: 9px; padding: 4px 8px; border-radius: 3px; font-weight: bold;
  border: 1px solid var(--cyan); color: var(--cyan); background: rgba(0, 240, 255, 0.1);
  transition: all 0.3s;
}
.status-badge.active {
  border-color: var(--yellow); color: #000; background: var(--yellow); box-shadow: 0 0 12px var(--yellow);
}
.video-toggle-btn {
  font-size: 9px; padding: 4px 8px; border-radius: 3px; font-weight: bold;
  border: 1px solid var(--border); color: var(--subtext); background: rgba(14, 22, 38, 0.8);
  cursor: pointer; transition: all 0.2s;
}
.video-toggle-btn.on { color: var(--cyan); border-color: var(--cyan); }

/* Floating in-app toast */
#cyberToast {
  display: none; position: fixed; top: 12px; left: 16px; right: 16px; z-index: 9999;
  padding: 12px 16px; border-radius: 6px; font-size: 12px; font-weight: bold;
  align-items: center; gap: 10px; box-shadow: 0 4px 25px rgba(0,0,0,0.85);
  pointer-events: none;
}
#cyberToast.show { display: flex; }
#cyberToast.success { background: #064E3B; border: 1px solid var(--green); color: #A7F3D0; }
#cyberToast.error { background: #881337; border: 1px solid var(--red); color: #FECDD3; }
#cyberToast.info { background: #0E2A47; border: 1px solid var(--cyan); color: #BAE6FD; }
#cyberToast.warn { background: #713F12; border: 1px solid var(--yellow); color: #FEF08A; }

/* Tabs */
.tabs { display: flex; gap: 6px; padding: 10px 16px 4px 16px; }
.tab-btn {
  flex: 1; padding: 10px 6px; background: var(--panel); border: 1px solid var(--border);
  color: var(--subtext); font-size: 10px; font-weight: 800; text-transform: uppercase;
  border-radius: 4px; cursor: pointer; text-align: center; white-space: nowrap;
  transition: all 0.2s; backdrop-filter: blur(6px);
}
.tab-btn.active {
  background: var(--cyan); color: #000; border-color: var(--cyan);
  box-shadow: 0 0 12px rgba(0, 240, 255, 0.4);
}

.container { padding: 10px 16px; }

/* Banner: 100% Standalone Phone Mode */
.standalone-badge-bar {
  background: linear-gradient(90deg, rgba(0, 240, 255, 0.15), rgba(252, 238, 10, 0.15));
  border: 1px solid var(--cyan);
  border-radius: 6px;
  padding: 8px 12px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.standalone-badge-text { font-size: 11px; font-weight: bold; color: var(--yellow); letter-spacing: 0.5px; }
.standalone-badge-sub { font-size: 9px; color: var(--cyan); }

/* Active Simulation Card */
.active-sim-panel {
  display: none;
  background: linear-gradient(135deg, rgba(20, 28, 48, 0.98), rgba(10, 15, 26, 0.99));
  border: 2px solid var(--yellow);
  border-radius: 6px; padding: 14px; margin-bottom: 14px;
  box-shadow: 0 0 25px rgba(252, 238, 10, 0.25);
  backdrop-filter: blur(8px);
}
.sim-title { font-size: 15px; font-weight: bold; color: var(--yellow); margin-bottom: 2px; }
.sim-timer { font-size: 30px; font-weight: 900; color: #FFF; font-family: monospace; margin: 6px 0; text-shadow: 0 0 10px var(--cyan); }
.sim-progress-bar { width: 100%; height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; overflow: hidden; margin-bottom: 10px; }
.sim-progress-fill { width: 0%; height: 100%; background: linear-gradient(90deg, var(--cyan), var(--yellow)); transition: width 1s linear; }

/* Discord Presence Live Box */
.discord-activity-box {
  background: rgba(6, 78, 59, 0.45);
  border: 1px solid var(--green);
  border-radius: 6px;
  padding: 10px 12px;
  margin: 10px 0;
  box-shadow: 0 0 15px rgba(0, 255, 102, 0.15);
  transition: all 0.3s;
}
.discord-activity-box.connecting {
  background: rgba(113, 63, 18, 0.45);
  border-color: var(--yellow);
}
.discord-activity-box.error {
  background: rgba(136, 19, 55, 0.45);
  border-color: var(--red);
}
.pulse-dot {
  width: 10px; height: 10px; border-radius: 50%;
  background: var(--green);
  box-shadow: 0 0 8px var(--green);
  display: inline-block;
  animation: pulse 1.5s infinite;
}
.pulse-dot.yellow { background: var(--yellow); box-shadow: 0 0 8px var(--yellow); }
.pulse-dot.red { background: var(--red); box-shadow: 0 0 8px var(--red); }
@keyframes pulse {
  0% { transform: scale(0.9); opacity: 0.7; }
  50% { transform: scale(1.2); opacity: 1; box-shadow: 0 0 14px var(--green); }
  100% { transform: scale(0.9); opacity: 0.7; }
}

/* Config Cards */
.config-card {
  background: var(--panel); border: 1px solid var(--border);
  border-radius: 6px; padding: 14px; margin-bottom: 14px;
  backdrop-filter: blur(8px);
}
.config-card h3 { font-size: 12px; color: var(--cyan); margin-bottom: 8px; text-transform: uppercase; letter-spacing: 1px; }

.token-status {
  padding: 10px 12px; border-radius: 4px; font-size: 11px; margin-bottom: 10px;
  background: rgba(14, 22, 38, 0.9); border: 1px solid var(--border);
  line-height: 1.4;
}
.token-status.success { border-color: var(--green); background: rgba(0, 255, 102, 0.15); color: #A7F3D0; }
.token-status.error { border-color: var(--red); background: rgba(255, 0, 60, 0.15); color: #FECDD3; }

.token-input-row { display: flex; gap: 6px; margin-bottom: 10px; }
.config-input {
  flex: 1; padding: 10px 12px; background: rgba(5, 8, 16, 0.95);
  border: 1px solid rgba(0, 240, 255, 0.35); color: #FFF; border-radius: 4px;
  font-size: 12px; font-family: monospace; outline: none;
  user-select: text !important; -webkit-user-select: text !important;
}
.config-input:focus { border-color: var(--cyan); box-shadow: 0 0 10px rgba(0, 240, 255, 0.5); }

/* Buttons */
.btn {
  padding: 10px 14px; font-size: 11px; font-weight: bold; text-transform: uppercase;
  border-radius: 4px; cursor: pointer; border: none; letter-spacing: 1px;
  transition: transform 0.1s, opacity 0.2s, background 0.2s;
  display: inline-flex; align-items: center; justify-content: center;
}
.btn:active { transform: scale(0.96); filter: brightness(1.2); }
.btn:disabled { opacity: 0.6; cursor: not-allowed; }
.btn-primary { background: var(--cyan); color: #000; box-shadow: 0 0 10px rgba(0, 240, 255, 0.4); }
.btn-yellow { background: var(--yellow); color: #000; box-shadow: 0 0 10px rgba(252, 238, 10, 0.4); }
.btn-red { background: var(--red); color: #FFF; box-shadow: 0 0 10px rgba(255, 0, 60, 0.4); }
.btn-outline { background: transparent; border: 1px solid var(--border); color: var(--cyan); }
.btn-icon { padding: 8px 10px; font-size: 13px; }

/* User Quests Section */
.user-quests-box {
  background: rgba(14, 22, 38, 0.95);
  border: 1px solid var(--yellow);
  border-radius: 6px;
  padding: 12px;
  margin-bottom: 14px;
}
.user-quests-header {
  display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;
}
.user-quests-title { font-size: 11px; font-weight: bold; color: var(--yellow); letter-spacing: 1px; }

/* Category Chips */
.chips-container {
  display: flex; gap: 6px; overflow-x: auto; padding-bottom: 8px; margin-bottom: 8px;
  scrollbar-width: none;
}
.chips-container::-webkit-scrollbar { display: none; }
.chip {
  padding: 6px 12px; background: rgba(14, 22, 38, 0.85); border: 1px solid rgba(0, 240, 255, 0.2);
  border-radius: 14px; font-size: 11px; font-weight: 600; color: var(--subtext);
  white-space: nowrap; cursor: pointer; transition: all 0.2s;
}
.chip.active {
  background: rgba(0, 240, 255, 0.22); border-color: var(--cyan); color: var(--cyan);
  box-shadow: 0 0 8px rgba(0, 240, 255, 0.3);
}

/* Search Row */
.search-row {
  display: flex; gap: 6px; align-items: center; margin-bottom: 8px;
}
.search-input {
  flex: 1; padding: 10px 12px; background: rgba(14, 20, 34, 0.95);
  border: 1px solid var(--border); color: #FFF; border-radius: 4px;
  font-size: 12px; outline: none;
  user-select: text !important; -webkit-user-select: text !important;
}
.search-input:focus { border-color: var(--cyan); box-shadow: 0 0 10px rgba(0, 240, 255, 0.35); }
.search-clear-btn {
  padding: 9px 12px; background: rgba(20, 30, 50, 0.8); border: 1px solid var(--border);
  color: var(--subtext); border-radius: 4px; cursor: pointer; font-size: 11px;
}

.search-summary {
  font-size: 10px; color: var(--cyan); margin-bottom: 10px; display: flex; justify-content: space-between;
}

/* Game Grid & Cards */
.game-grid { display: flex; flex-direction: column; gap: 10px; }
.game-card {
  background: var(--card); border: 1px solid rgba(0, 240, 255, 0.2);
  border-left: 4px solid var(--cyan); border-radius: 6px; padding: 12px;
  display: flex; align-items: center; justify-content: space-between; gap: 10px;
  backdrop-filter: blur(6px);
}
.game-card.quest { border-left-color: var(--yellow); }
.game-card.popular { border-left-color: var(--purple); }
.game-card.custom { border-left-color: var(--green); }
.game-info { flex: 1; min-width: 0; }
.game-name { font-size: 13px; font-weight: bold; color: #FFF; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.game-sub { font-size: 10px; color: var(--subtext); margin-top: 2px; }
.game-badge {
  display: inline-block; font-size: 9px; padding: 2px 6px; border-radius: 2px;
  background: rgba(0, 240, 255, 0.15); color: var(--cyan); font-weight: bold; margin-top: 4px;
}
.game-badge.quest-badge { background: rgba(252, 238, 10, 0.15); color: var(--yellow); }
.game-badge.popular-badge { background: rgba(168, 85, 247, 0.2); color: #C084FC; }
.game-badge.custom-badge { background: rgba(0, 255, 102, 0.15); color: var(--green); }
.card-actions { display: flex; align-items: center; gap: 6px; }

/* Interactive Suggestions Dropdown */
.suggestions-dropdown {
  position: absolute;
  top: 100%; left: 0; right: 0;
  max-height: 180px; overflow-y: auto;
  background: #090D15;
  border: 1px solid var(--cyan);
  border-radius: 4px;
  z-index: 1050;
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.95);
}
.suggestion-item {
  padding: 8px 10px;
  border-bottom: 1px solid rgba(0, 240, 255, 0.15);
  cursor: pointer;
  display: flex; justify-content: space-between; align-items: center;
}
.suggestion-item:hover, .suggestion-item:active {
  background: rgba(0, 240, 255, 0.2);
  color: var(--yellow);
}
.suggestion-name { font-size: 12px; font-weight: bold; color: #FFF; }
.suggestion-id { font-size: 10px; font-family: monospace; color: var(--cyan); }

/* On-screen Live Debug Log */
.debug-box {
  margin-top: 20px; background: rgba(5, 8, 16, 0.9); border: 1px solid rgba(0, 240, 255, 0.2);
  border-radius: 4px; padding: 10px; font-family: monospace; font-size: 10px;
  color: #94A3B8; max-height: 140px; overflow-y: auto;
}
.debug-line { margin-bottom: 4px; word-break: break-all; }
.debug-line.ok { color: var(--green); }
.debug-line.err { color: var(--red); }
.debug-line.act { color: var(--cyan); }

/* Modal overlay */
.modal {
  display: none; position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
  background: rgba(0, 0, 0, 0.88); z-index: 1000;
  align-items: center; justify-content: center; padding: 16px;
  backdrop-filter: blur(6px);
}
.modal-content {
  background: #0E1626; border: 2px solid var(--cyan); border-radius: 8px;
  padding: 18px; width: 100%; max-width: 440px; box-shadow: 0 0 35px rgba(0, 240, 255, 0.35);
}
.modal-title { font-size: 14px; font-weight: bold; color: var(--yellow); margin-bottom: 12px; letter-spacing: 1px; }
.modal-text { font-size: 11px; color: #CBD5E1; line-height: 1.5; margin-bottom: 14px; }
</style>
</head>
<body>

<!-- Cyberpunk Background Video -->
<video id="bgVideo" autoplay loop muted playsinline preload="auto">
  <source src="fonpril.mp4" type="video/mp4">
</video>
<div class="bg-overlay"></div>

<div id="cyberToast">
  <span id="toastIcon">⚡</span>
  <span id="toastMsg">Готово</span>
</div>

<header>
  <div>
    <div class="logo-title">ESHKERI // MOBILE</div>
    <div class="logo-sub">100% STANDALONE DISCORD QUEST SPONSOR v2.7</div>
  </div>
  <div class="header-actions">
    <button class="video-toggle-btn on" id="btnToggleBg" onclick="toggleVideoBg()">🎬 ФОН: ВКЛ</button>
    <div class="status-badge" id="hudStatusBadge">STANDBY</div>
  </div>
</header>

<div class="tabs">
  <div class="tab-btn active" id="tabQuests" onclick="switchTab('quests')">⚡ КВЕСТЫ (БЕЗ ПК)</div>
  <div class="tab-btn" id="tabRemote" onclick="switchTab('remote')">📡 ПК (WI-FI)</div>
  <div class="tab-btn" id="tabStandalone" onclick="switchTab('standalone')">⏱️ ТАЙМЕР</div>
</div>

<div class="container">

  <!-- Standalone Mobile Info Bar -->
  <div class="standalone-badge-bar">
    <div>
      <div class="standalone-badge-text">📱 100% АВТОНОМНЫЙ РЕЖИМ (ПК НЕ НУЖЕН)</div>
      <div class="standalone-badge-sub">Автоматическая запись на квесты, Heartbeat прогресса и трансляция в Discord прямо с телефона</div>
    </div>
    <span style="font-size: 16px;">⚡</span>
  </div>

  <!-- Active Simulation Panel -->
  <div class="active-sim-panel" id="activeSimPanel">
    <div style="display: flex; justify-content: space-between; align-items: center;">
      <div>
        <div class="sim-title" id="activeGameTitle">ВЫПОЛНЕНИЕ КВЕСТА...</div>
        <div style="font-size: 10px; color: var(--cyan);" id="activeGameSub">АВТОМАТИЧЕСКАЯ ОТПРАВКА HEARTBEATS В DISCORD API</div>
      </div>
      <button class="btn btn-red" onclick="stopSimulation()">СТОП</button>
    </div>

    <!-- Live Discord Presence Status Box -->
    <div id="discordActivityBox" class="discord-activity-box connecting">
      <div style="display: flex; align-items: center; gap: 8px;">
        <span class="pulse-dot yellow" id="discordPulseDot"></span>
        <span id="discordActivityTitle" style="font-weight: bold; font-size: 12px; color: var(--yellow);">ПОДКЛЮЧЕНИЕ К DISCORD GATEWAY...</span>
      </div>
      <div id="discordActivityDesc" style="font-size: 11px; color: #CBD5E1; margin-top: 4px;">
        Статус в Discord: Установка активности «Играет в...»
      </div>
      <div id="discordGatewayStatus" style="font-size: 10px; color: var(--cyan); margin-top: 2px;">
        Сервер: wss://gateway.discord.gg (Opcode 3 Presence + API Heartbeats)
      </div>
    </div>

    <div class="sim-timer" id="activeSimTimer">00:00</div>
    <div class="sim-progress-bar">
      <div class="sim-progress-fill" id="activeProgressBar"></div>
    </div>
    <div style="font-size: 10px; color: var(--subtext); display: flex; justify-content: space-between;">
      <span id="activeModeLabel">HEARTBEAT В DISCORD: КАЖДЫЕ 20 СЕК</span>
      <span id="activeTargetLabel">ЦЕЛЬ: 15:00 МИН</span>
    </div>
  </div>

  <!-- Quests & Games Tab (Mode 1 - 100% Standalone Mobile) -->
  <div id="questsConfigCard">
    <div class="config-card">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <h3>🔑 АВТОРИЗАЦИЯ DISCORD (ТОКЕН С ТЕЛЕФОНА)</h3>
        <button class="btn btn-outline" style="padding: 3px 8px; font-size: 9px;" onclick="showTokenHelp()">ИНФО</button>
      </div>

      <div id="tokenStatusBanner" class="token-status">
        <span>⚠️ Вставьте токен Discord для автоматического выполнения квестов без ПК</span>
      </div>

      <div class="token-input-row">
        <input type="password" class="config-input" id="discordTokenInput" placeholder="Вставьте токен Discord">
        <button class="btn btn-outline btn-icon" title="Показать/скрыть токен" onclick="toggleTokenVisibility()">👁️</button>
        <button class="btn btn-primary btn-icon" title="Вставить из буфера" onclick="pasteFromClipboard()">📋 ВСТАВИТЬ</button>
      </div>

      <div style="display: flex; gap: 8px;">
        <button class="btn btn-yellow" id="btnVerifyToken" style="flex: 1;" onclick="verifyToken()">ПРОВЕРИТЬ ТОКЕН</button>
        <button class="btn btn-outline" onclick="fetchUserQuests()">ОБНОВИТЬ КВЕСТЫ</button>
      </div>
    </div>

    <!-- Live Account Quests Box (@me) -->
    <div class="user-quests-box" id="userQuestsBox" style="display: none;">
      <div class="user-quests-header">
        <span class="user-quests-title">🎯 АКТИВНЫЕ КВЕСТЫ ВАШЕГО АККАУНТА (DISCORD @ME)</span>
        <button class="btn btn-outline" style="padding: 2px 6px; font-size: 9px;" onclick="fetchUserQuests()">🔄 ОБНОВИТЬ</button>
      </div>
      <div id="userQuestsList" style="display: flex; flex-direction: column; gap: 8px;"></div>
    </div>

    <!-- Category Chips (Exact PC Experience) -->
    <div class="chips-container" id="categoryChips">
      <div class="chip active" onclick="selectCategory('all', this)">⭐ ВСЕ (24k+)</div>
      <div class="chip" onclick="selectCategory('custom', this)">💾 МОИ ИГРЫ</div>
      <div class="chip" onclick="selectCategory('quests', this)">★ ТОП КВЕСТЫ</div>
      <div class="chip" onclick="selectCategory('popular', this)">🔥 ПОПУЛЯРНЫЕ</div>
      <div class="chip" onclick="selectCategory('shooters', this)">🎯 ШУТЕРЫ / ОНЛАЙН</div>
      <div class="chip" onclick="selectCategory('rpg', this)">⚔️ RPG</div>
      <div class="chip" onclick="selectCategory('survival', this)">🌲 ВЫЖИВАНИЕ</div>
    </div>

    <!-- Search Box like in PC Version -->
    <div class="search-row">
      <input type="text" class="search-input" id="gameSearchInput" placeholder="🔍 Поиск по 24 300+ играм (Marvel, GTA, CS, Genshin, Rust)..." oninput="onSearchInput()">
      <button class="search-clear-btn" title="Очистить" onclick="clearSearch()">✖</button>
      <button class="btn btn-yellow" style="padding: 8px 12px; font-size: 11px; white-space: nowrap;" onclick="showAddGameModal()">+ ДОБАВИТЬ</button>
    </div>

    <div class="search-summary">
      <span id="searchResultCount">Загрузка каталога игр...</span>
      <span id="dbSourceLabel" style="color: var(--subtext);">База Discord (24 324 игры)</span>
    </div>

    <!-- Dynamic Game Cards Grid -->
    <div class="game-grid" id="gamesGrid"></div>
  </div>

  <!-- Remote PC Bridge Tab (Mode 2) -->
  <div id="remoteConfigCard" style="display: none;">
    <div class="config-card">
      <h3>📡 УДАЛЕННОЕ УПРАВЛЕНИЕ ПК (WI-FI)</h3>
      <p style="font-size: 11px; color: var(--subtext); margin-bottom: 8px;">
        Используйте эту вкладку, только если вы хотите управлять спуфером на включенном ПК по Wi-Fi.
      </p>
      <input type="text" class="config-input" id="pcIpInput" placeholder="IP компьютера (например: 192.168.1.103:8888)">
      <button class="btn btn-yellow" style="width: 100%; margin-bottom: 8px;" onclick="testPcConnection()">ПРОВЕРИТЬ СВЯЗЬ С ПК</button>
      <button class="btn btn-outline" style="width: 100%;" onclick="sendRemoteStop()">ОСТАНОВИТЬ СПУФЕР НА ПК</button>
    </div>
  </div>

  <!-- Standalone Timer Tab (Mode 3) -->
  <div id="standaloneConfigCard" style="display: none;">
    <div class="config-card">
      <h3>⏱️ АВТОНОМНЫЙ ТАЙМЕР</h3>
      <p style="font-size: 11px; color: var(--subtext); margin-bottom: 12px;">
        15-минутный таймер со звуковым сопровождением завершения квеста.
      </p>
      <button class="btn btn-primary" style="width: 100%;" onclick="startStandaloneTimer()">СТАРТ ТАЙМЕРА 15 МИН</button>
    </div>
  </div>

  <!-- Live Event Log -->
  <div class="debug-box" id="debugBox">
    <div class="debug-line act">[SYSTEM] Eshkeri Mobile v2.7 готов к работе (100% Standalone Phone Engine)</div>
  </div>

</div>

<!-- Convenient Add Game Modal (Exact PC Version Behavior with Live Auto-Suggestions) -->
<div class="modal" id="addGameModal">
  <div class="modal-content">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
      <div class="modal-title">ДОБАВИТЬ ИГРУ В КАТАЛОГ</div>
      <button class="search-clear-btn" onclick="closeModal('addGameModal')">✖</button>
    </div>

    <label style="font-size: 11px; color: var(--cyan); margin-bottom: 4px; display: block; font-weight: bold;">
      Название игры (поиск по 24 300+ играм Discord):
    </label>
    <div style="position: relative; margin-bottom: 6px;">
      <input type="text" class="config-input" id="newGameName" placeholder="например: GTA, Stalker, Cyberpunk, Witcher..." oninput="onAddGameSearchInput()" autocomplete="off">
      <div id="addGameSuggestions" class="suggestions-dropdown" style="display: none;"></div>
    </div>

    <div id="addGameMatchStatus" style="font-size: 10px; color: var(--subtext); margin-bottom: 10px;">
      ℹ Введите название — ID заполнится автоматически из базы Discord
    </div>

    <label style="font-size: 11px; color: var(--cyan); margin-bottom: 4px; display: block; font-weight: bold;">
      Discord Application ID (заполняется автоматически):
    </label>
    <input type="text" class="config-input" id="newGameAppId" placeholder="например: 1445160676522856458" style="margin-bottom: 10px;">

    <label style="font-size: 11px; color: var(--cyan); margin-bottom: 4px; display: block; font-weight: bold;">
      Длительность квеста (минут):
    </label>
    <input type="number" class="config-input" id="newGameDuration" value="15" min="1" max="180" style="margin-bottom: 14px;">

    <div style="display: flex; gap: 8px;">
      <button class="btn btn-yellow" style="flex: 1;" onclick="saveCustomGame(false)">💾 СОХРАНИТЬ В КАТАЛОГ</button>
      <button class="btn btn-primary" style="flex: 1;" onclick="saveCustomGame(true)">▶ СРАЗУ ИГРАТЬ</button>
    </div>
  </div>
</div>

<!-- Token Info Modal -->
<div class="modal" id="tokenHelpModal">
  <div class="modal-content">
    <div class="modal-title">КАК ПОЛУЧИТЬ ТОКЕН DISCORD</div>
    <div class="modal-text">
      1. Откройте <b>discord.com/app</b> в браузере (на телефоне в режиме «Версия для ПК» или на ПК).<br>
      2. Нажмите F12 или откройте консоль разработчика -> вкладка <b>Сеть (Network)</b>.<br>
      3. В фильтр введите <b>/api</b> и обновите страницу.<br>
      4. Кликните по любому запросу (например, <i>@me</i> или <i>messages</i>).<br>
      5. В разделе <b>Headers</b> найдите <b>authorization</b> и скопируйте значение.<br><br>
      <span style="color: var(--yellow);">💡 ПК НЕ НУЖЕН: после ввода токена телефон выполняет квесты полностью самостоятельно!</span><br><br>
      <span style="color: var(--cyan);">🌐 Для пользователей из РФ: серверы Discord заблокированы в РФ, поэтому для выполнения квестов на телефоне должен быть включен VPN!</span>
    </div>
    <button class="btn btn-primary" style="width: 100%;" onclick="closeModal('tokenHelpModal')">ПОНЯТНО</button>
  </div>
</div>

<script>
// --- GLOBAL ERROR CATCHER ---
window.onerror = function(msg, url, line) {
  var box = document.getElementById("debugBox");
  if (box) {
    var d = document.createElement("div");
    d.className = "debug-line err";
    d.innerText = "[JS ERROR] " + msg + " (" + line + ")";
    box.appendChild(d);
  }
  return false;
};

// --- LIVE DEBUG LOG ---
function logEvent(msg, type) {
  var box = document.getElementById("debugBox");
  if (!box) return;
  var d = new Date();
  var ts = d.toTimeString().split(' ')[0];
  var line = document.createElement("div");
  line.className = "debug-line " + (type || "act");
  line.innerText = "[" + ts + "] " + msg;
  box.appendChild(line);
  box.scrollTop = box.scrollHeight;
}

// --- AUDIO SYNTHESIZER ---
var audioCtx = null;
function getAudio() {
  try {
    var AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!audioCtx && AudioContext) audioCtx = new AudioContext();
    if (audioCtx && audioCtx.state === 'suspended') audioCtx.resume();
  } catch(e){}
  return audioCtx;
}
function sfxGlitch() {
  try {
    var ctx = getAudio(); if (!ctx) return;
    var osc = ctx.createOscillator(); var gain = ctx.createGain();
    osc.type = 'sawtooth'; osc.frequency.setValueAtTime(220, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(880, ctx.currentTime + 0.1);
    gain.gain.setValueAtTime(0.2, ctx.currentTime); gain.gain.linearRampToValueAtTime(0.01, ctx.currentTime + 0.1);
    osc.connect(gain); gain.connect(ctx.destination);
    osc.start(); osc.stop(ctx.currentTime + 0.1);
  } catch(e){}
}
function sfxLaunch() {
  try {
    var ctx = getAudio(); if (!ctx) return;
    var osc = ctx.createOscillator(); var gain = ctx.createGain();
    osc.type = 'sine'; osc.frequency.setValueAtTime(440, ctx.currentTime);
    osc.frequency.exponentialRampToValueAtTime(1200, ctx.currentTime + 0.25);
    gain.gain.setValueAtTime(0.3, ctx.currentTime); gain.gain.linearRampToValueAtTime(0.01, ctx.currentTime + 0.25);
    osc.connect(gain); gain.connect(ctx.destination);
    osc.start(); osc.stop(ctx.currentTime + 0.25);
  } catch(e){}
}
function sfxComplete() {
  try {
    var ctx = getAudio(); if (!ctx) return;
    [523.25, 659.25, 783.99, 1046.50].forEach(function(freq, i) {
      var osc = ctx.createOscillator(); var gain = ctx.createGain();
      osc.type = 'triangle'; osc.frequency.value = freq;
      gain.gain.setValueAtTime(0.2, ctx.currentTime + i * 0.1);
      gain.gain.linearRampToValueAtTime(0.01, ctx.currentTime + i * 0.1 + 0.25);
      osc.connect(gain); gain.connect(ctx.destination);
      osc.start(ctx.currentTime + i * 0.1); osc.stop(ctx.currentTime + i * 0.1 + 0.3);
    });
  } catch(e){}
}

// --- NOTIFICATION TOAST ---
var toastTimeout = null;
function showCyberToast(msg, type) {
  type = type || 'info';
  var t = document.getElementById("cyberToast");
  var m = document.getElementById("toastMsg");
  var ic = document.getElementById("toastIcon");
  if (!t || !m) return;

  var icons = { success: '✅', error: '❌', info: '⚡', warn: '⚠️' };
  ic.innerText = icons[type] || '⚡';
  m.innerText = msg;
  t.className = 'show ' + type;

  if (toastTimeout) clearTimeout(toastTimeout);
  toastTimeout = setTimeout(function() {
    t.className = '';
  }, 4000);

  if (window.AndroidBridge && window.AndroidBridge.showToast) {
    try { window.AndroidBridge.showToast(msg); } catch(e){}
  }
}

// --- SAFE STORAGE ---
var memStorage = {};
var storage = {
  get: function(k, def) {
    try {
      if (window.localStorage) {
        var v = localStorage.getItem(k);
        return v !== null ? v : def;
      }
    } catch(e){}
    return memStorage[k] !== undefined ? memStorage[k] : def;
  },
  set: function(k, v) {
    try {
      if (window.localStorage) {
        localStorage.setItem(k, v);
      }
    } catch(e){}
    memStorage[k] = v;
  }
};

// --- BACKGROUND VIDEO CONTROLLER ---
function setVideoBackground(url) {
  var v = document.getElementById("bgVideo");
  if (v && url) {
    v.src = url;
    v.play().catch(function(err){
      console.log("Auto-play blocked, waiting for touch:", err);
    });
  }
}

function toggleVideoBg() {
  var v = document.getElementById("bgVideo");
  var btn = document.getElementById("btnToggleBg");
  if (!v) return;
  if (v.paused) {
    v.play();
    btn.className = "video-toggle-btn on";
    btn.innerText = "🎬 ФОН: ВКЛ";
    showCyberToast("🎬 Фоновое видео запущено", "info");
  } else {
    v.pause();
    btn.className = "video-toggle-btn";
    btn.innerText = "🎬 ФОН: ВЫКЛ";
    showCyberToast("⏸️ Фоновое видео на паузе", "info");
  }
}

// --- TOKEN SANITIZER ---
function sanitizeToken(t) {
  if (!t) return "";
  var s = t.trim();
  s = s.replace(/^authorization:\s*/i, "");
  s = s.replace(/^token:\s*/i, "");
  s = s.replace(/^["']|["']$/g, "");
  return s.trim();
}

function toggleTokenVisibility() {
  var inp = document.getElementById("discordTokenInput");
  inp.type = (inp.type === "password" ? "text" : "password");
}

function pasteFromClipboard() {
  sfxGlitch();
  logEvent("Запрос буфера обмена...", "act");

  if (window.AndroidBridge && window.AndroidBridge.getClipboard) {
    try {
      var clip = window.AndroidBridge.getClipboard();
      if (clip && clip.trim().length > 0) {
        var clean = sanitizeToken(clip);
        document.getElementById("discordTokenInput").value = clean;
        saveToken();
        logEvent("Токен вставлен из буфера (" + clean.length + " символов)", "ok");
        showCyberToast("📋 Токен вставлен из буфера!", "success");
        verifyToken();
        return;
      }
    } catch(err) {
      console.warn("Native clip err:", err);
    }
  }

  try {
    var manual = prompt("Вставьте ваш Discord токен:");
    if (manual) {
      var clean = sanitizeToken(manual);
      document.getElementById("discordTokenInput").value = clean;
      saveToken();
      logEvent("Токен введен вручную (" + clean.length + " символов)", "ok");
      showCyberToast("📋 Токен сохранен!", "success");
      verifyToken();
    }
  } catch(e) {
    showCyberToast("ℹ️ Удерживайте поле ввода и выберите «Вставить»", "info");
  }
}

// --- ASYNCHRONOUS HTTP REQUEST ENGINE ---
function nativeRequest(url, method, token, body, callback) {
  var cleanTok = sanitizeToken(token);

  setTimeout(function() {
    if (window.AndroidBridge && window.AndroidBridge.httpRequest) {
      try {
        var raw = window.AndroidBridge.httpRequest(url, method || "GET", cleanTok || "", body || null);
        if (raw) {
          var parsed = JSON.parse(raw);
          callback(parsed);
          return;
        }
      } catch(err) {
        console.warn("Bridge attempt error, falling back to fetch:", err);
      }
    }

    var headers = { "Content-Type": "application/json", "Accept": "*/*" };
    if (cleanTok) headers["Authorization"] = cleanTok;

    var controller = (window.AbortController ? new AbortController() : null);
    var timer = controller ? setTimeout(function(){ controller.abort(); }, 8000) : null;

    fetch(url, {
      method: method || "GET",
      headers: headers,
      body: (method === "POST" && body) ? body : undefined,
      signal: controller ? controller.signal : undefined
    })
    .then(function(res) {
      if (timer) clearTimeout(timer);
      return res.text().then(function(text) {
        var d = null;
        try { d = JSON.parse(text); } catch(e) { d = text; }
        callback({ status: res.status, data: d });
      });
    })
    ["catch"](function(err) {
      if (timer) clearTimeout(timer);
      callback({ status: -1, error: err.toString() });
    });
  }, 30);
}

// --- CURATED TOP GAMES & QUESTS CATALOG ---
var CURATED_GAMES = [
  { name: "Marvel Rivals", id: "1314395942253756416", cat: "quests", sub: "Discord Quest / Drops & Exclusive Orbs", badge: "★ DISCORD QUEST" },
  { name: "ANIIMO GLOBAL LAUNCH", id: "1468082130474111047", cat: "quests", sub: "Официальный Discord Quest / Steam", badge: "★ DISCORD QUEST" },
  { name: "FORGOTTEN ISLAND", id: "1468199201984217088", cat: "quests", sub: "Discord Quest / Survival Adventure", badge: "★ DISCORD QUEST" },
  { name: "Rust", id: "424076724602601472", cat: "quests", sub: "Discord Quest / Facepunch Studios", badge: "★ DISCORD QUEST" },
  { name: "Grand Theft Auto VI", id: "1445160676522856458", cat: "popular", sub: "Rockstar Games / Vice City", badge: "🔥 ТОП ХИТ" },
  { name: "Grand Theft Auto V", id: "425442502758236170", cat: "popular", sub: "Rockstar Games / GTA Online", badge: "🔥 ТОП ХИТ" },
  { name: "Cyberpunk 2077", id: "787443973538971748", cat: "popular", sub: "Night City RPG / CD PROJEKT RED", badge: "🔥 ТОП ХИТ" },
  { name: "Counter-Strike 2", id: "733878259275038820", cat: "shooters", sub: "Valve Competitive FPS", badge: "🔥 ТОП ХИТ" },
  { name: "Dota 2", id: "419736869408440320", cat: "popular", sub: "Valve MOBA / The International", badge: "🔥 ТОП ХИТ" },
  { name: "Minecraft", id: "432980957394370572", cat: "popular", sub: "Mojang Studios / Sandbox", badge: "🔥 ТОП ХИТ" },
  { name: "Roblox", id: "363445589247131668", cat: "popular", sub: "Roblox Corporation", badge: "🔥 ТОП ХИТ" },
  { name: "Genshin Impact", id: "762434991303950386", cat: "rpg", sub: "HoYoverse / Teyvat Adventure", badge: "⚔️ RPG" },
  { name: "Honkai: Star Rail", id: "1046985476483125278", cat: "rpg", sub: "HoYoverse / Astral Express", badge: "⚔️ RPG" },
  { name: "Zenless Zone Zero", id: "1257912444647669862", cat: "rpg", sub: "HoYoverse / New Eridu", badge: "⚔️ RPG" },
  { name: "Arknights: Endfield", id: "1461154307171811401", cat: "rpg", sub: "Hypergryph / Talos-II RPG", badge: "⚔️ RPG" },
  { name: "Valorant", id: "700136079562375258", cat: "shooters", sub: "Riot Games / Tactical Shooter", badge: "🎯 ШУТЕР" },
  { name: "Apex Legends", id: "543761174243606529", cat: "shooters", sub: "Respawn Entertainment / EA", badge: "🎯 ШУТЕР" },
  { name: "League of Legends", id: "401518687463948290", cat: "popular", sub: "Riot Games / Summoner's Rift", badge: "🔥 ТОП ХИТ" },
  { name: "Fortnite", id: "432980957394370570", cat: "shooters", sub: "Epic Games / Battle Royale", badge: "🎯 ШУТЕР" },
  { name: "Overwatch 2", id: "356875221078245376", cat: "shooters", sub: "Blizzard Entertainment", badge: "🎯 ШУТЕР" },
  { name: "Rainbow Six Siege", id: "356876590342340608", cat: "shooters", sub: "Ubisoft / Tactical FPS", badge: "🎯 ШУТЕР" },
  { name: "Warframe", id: "425446549221539850", cat: "shooters", sub: "Digital Extremes / Sci-Fi Ninja", badge: "🎯 ШУТЕР" },
  { name: "Dead by Daylight", id: "357607133254254632", cat: "survival", sub: "Behaviour / Asymmetric Horror", badge: "🌲 ВЫЖИВАНИЕ" },
  { name: "Escape from Tarkov", id: "406637848297472017", cat: "survival", sub: "Battlestate Games / Hardcore FPS", badge: "🌲 ВЫЖИВАНИЕ" },
  { name: "The Witcher 3: Wild Hunt", id: "359510249486417920", cat: "rpg", sub: "CD PROJEKT RED / Geralt of Rivia", badge: "⚔️ RPG" },
  { name: "Elden Ring", id: "926578496464195614", cat: "rpg", sub: "FromSoftware / Lands Between", badge: "⚔️ RPG" },
  { name: "Baldur's Gate 3", id: "761002302306910248", cat: "rpg", sub: "Larian Studios / D&D RPG", badge: "⚔️ RPG" },
  { name: "Black Myth: Wukong", id: "1275338166681239613", cat: "rpg", sub: "Game Science / Destined One", badge: "⚔️ RPG" },
  { name: "Helldivers 2", id: "1196150244799516692", cat: "shooters", sub: "Arrowhead / Super Earth", badge: "🎯 ШУТЕР" },
  { name: "Palworld", id: "1198276709846437948", cat: "survival", sub: "Pocketpair / Monster Survival", badge: "🌲 ВЫЖИВАНИЕ" },
  { name: "Stardew Valley", id: "359509387670192128", cat: "survival", sub: "ConcernedApe / Farming & Life", badge: "🌲 ВЫЖИВАНИЕ" },
  { name: "Terraria", id: "425442340384145418", cat: "survival", sub: "Re-Logic / 2D Adventure", badge: "🌲 ВЫЖИВАНИЕ" },
  { name: "The Forest", id: "363409179668512788", cat: "survival", sub: "Endnight Games / Survival Horror", badge: "🌲 ВЫЖИВАНИЕ" },
  { name: "ARK: Survival Evolved", id: "356887282982191114", cat: "survival", sub: "Studio Wildcard / Dinosaurs", badge: "🌲 ВЫЖИВАНИЕ" },
  { name: "World of Tanks", id: "357607478105604096", cat: "shooters", sub: "Wargaming / Armored Warfare", badge: "🎯 ОНЛАЙН" },
  { name: "World of Warcraft", id: "356875762940379136", cat: "rpg", sub: "Blizzard Entertainment / MMORPG", badge: "⚔️ RPG" },
  { name: "Rocket League", id: "356877880938070016", cat: "popular", sub: "Psyonix / Soccar", badge: "🔥 ТОП ХИТ" },
  { name: "FEMBOY FUTA HOUSE", id: "1416830938263846973", cat: "quests", sub: "Discord Quest / Drops", badge: "★ DISCORD QUEST" }
];

var fullDetectableDb = [];
var customGames = [];
var activeUserQuests = [];
var selectedCategory = "all";

function loadCustomGames() {
  try {
    var raw = storage.get("eshk_custom_games", "[]");
    var parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) customGames = parsed;
  } catch(e){
    customGames = [];
  }
}

function saveCustomGames() {
  storage.set("eshk_custom_games", JSON.stringify(customGames));
}

// --- DISCORD GATEWAY WEBSOCKET ENGINE (RICH PRESENCE) ---
var discordWs = null;
var wsHeartbeatTimer = null;
var wsSeq = null;
var wsSessionId = null;
var wsActive = false;
var questHeartbeatTimer = null;

function connectDiscordGateway(game) {
  var token = sanitizeToken(document.getElementById("discordTokenInput").value);
  if (!token) {
    updateDiscordStatusUI("NO_TOKEN", game);
    showCyberToast("⚠️ Чтобы активность появилась в Discord, введите токен выше!", "warn");
    return;
  }

  closeDiscordGateway();

  updateDiscordStatusUI("CONNECTING", game);
  logEvent("[GATEWAY] Подключение к wss://gateway.discord.gg...", "act");

  try {
    discordWs = new WebSocket("wss://gateway.discord.gg/?v=9&encoding=json");

    discordWs.onopen = function() {
      logEvent("[GATEWAY] Соединение установлено, ожидание Hello...", "ok");
    };

    discordWs.onmessage = function(event) {
      try {
        var msg = JSON.parse(event.data);
        if (msg.s) wsSeq = msg.s;

        // Opcode 10: Hello -> start heartbeats & Identify
        if (msg.op === 10) {
          var interval = msg.d.heartbeat_interval;
          logEvent("[GATEWAY] Получен Hello, Heartbeat: " + interval + " мс", "ok");

          if (wsHeartbeatTimer) clearInterval(wsHeartbeatTimer);
          wsHeartbeatTimer = setInterval(function() {
            if (discordWs && discordWs.readyState === WebSocket.OPEN) {
              discordWs.send(JSON.stringify({ op: 1, d: wsSeq }));
            }
          }, interval);

          discordWs.send(JSON.stringify({ op: 1, d: wsSeq }));

          var startTime = Date.now() - (simSeconds * 1000);
          var identifyPayload = {
            op: 2,
            d: {
              token: token,
              capabilities: 16381,
              properties: {
                os: "Windows",
                browser: "Discord Client",
                release_channel: "stable",
                client_version: "1.0.9150",
                os_version: "10.0.19045",
                os_arch: "x64",
                system_locale: "ru-RU"
              },
              presence: {
                status: "online",
                since: 0,
                activities: [
                  {
                    name: game.name,
                    type: 0, // 0 = Playing ("Играет в ...")
                    application_id: String(game.client_id),
                    timestamps: {
                      start: startTime
                    },
                    flags: 1
                  }
                ],
                afk: false
              },
              compress: false,
              client_state: {
                guild_versions: {}
              }
            }
          };
          discordWs.send(JSON.stringify(identifyPayload));
          logEvent("[GATEWAY] Отправлен Identify («Играет в " + game.name + "», ID: " + game.client_id + ")", "act");
        }

        // Opcode 0: Dispatch
        if (msg.op === 0) {
          if (msg.t === "READY") {
            wsSessionId = msg.d.session_id;
            var userTag = msg.d.user.username;
            wsActive = true;
            logEvent("[GATEWAY] 🔥 DISCORD ПОДТВЕРДИЛ: " + userTag + " играет в «" + game.name + "»!", "ok");
            showCyberToast("🎮 Активность в Discord: Играет в " + game.name + "!", "success");
            updateDiscordStatusUI("ACTIVE", game, userTag);
            sfxLaunch();
          }
        }

        if (msg.op === 11) {
          // Heartbeat acknowledged by Discord
        }

        if (msg.op === 9) {
          logEvent("[GATEWAY] Недействительная сессия (Opcode 9)", "err");
        }

      } catch(parseErr) {
        console.warn("WS parse err:", parseErr);
      }
    };

    discordWs.onerror = function(err) {
      logEvent("[GATEWAY] Сбой WebSocket. Если вы в РФ — включите VPN на телефоне!", "err");
      updateDiscordStatusUI("ERROR", game);
      showCyberToast("⚠️ Ошибка Gateway Discord (проверьте VPN)!", "warn");
    };

    discordWs.onclose = function(ev) {
      logEvent("[GATEWAY] Соединение закрыто (код: " + ev.code + ")", "act");
      if (wsActive) {
        updateDiscordStatusUI("DISCONNECTED", game);
      }
      wsActive = false;
      if (wsHeartbeatTimer) clearInterval(wsHeartbeatTimer);
      wsHeartbeatTimer = null;
    };

  } catch(e) {
    logEvent("[GATEWAY] Ошибка подключения: " + e, "err");
  }
}

function updateDiscordStatusUI(state, game, userTag) {
  var box = document.getElementById("discordActivityBox");
  var dot = document.getElementById("discordPulseDot");
  var title = document.getElementById("discordActivityTitle");
  var desc = document.getElementById("discordActivityDesc");
  var statusLbl = document.getElementById("discordGatewayStatus");

  if (!box || !title || !desc) return;

  if (state === "ACTIVE") {
    box.className = "discord-activity-box";
    dot.className = "pulse-dot";
    title.innerText = "🟢 DISCORD АКТИВНОСТЬ: АКТИВНА";
    title.style.color = "var(--green)";
    desc.innerText = "В профиле " + (userTag ? userTag + " " : "") + "отображается: «Играет в " + game.name + "»";
    statusLbl.innerText = "Соединение: wss://gateway.discord.gg (Opcode 3 Presence • ОНЛАЙН НА ТЕЛЕФОНЕ)";
  } else if (state === "CONNECTING") {
    box.className = "discord-activity-box connecting";
    dot.className = "pulse-dot yellow";
    title.innerText = "🟡 ПОДКЛЮЧЕНИЕ К DISCORD GATEWAY...";
    title.style.color = "var(--yellow)";
    desc.innerText = "Отправка пакета Presence для игры: " + game.name;
    statusLbl.innerText = "Соединение: wss://gateway.discord.gg (Handshake...)";
  } else if (state === "NO_TOKEN") {
    box.className = "discord-activity-box error";
    dot.className = "pulse-dot red";
    title.innerText = "⚠️ ТОКЕН НЕ ВВЕДЕН";
    title.style.color = "var(--red)";
    desc.innerText = "Чтобы активность «Играет в...» появилась в профиле Discord, укажите токен выше!";
    statusLbl.innerText = "Режим: Локальный таймер (без сетевого статуса)";
  } else if (state === "ERROR") {
    box.className = "discord-activity-box error";
    dot.className = "pulse-dot red";
    title.innerText = "🔴 СБОЙ GATEWAY (ВКЛЮЧИТЕ VPN)";
    title.style.color = "var(--red)";
    desc.innerText = "Серверы Discord блокируются в РФ. Включите VPN на телефоне!";
    statusLbl.innerText = "Ошибка соединения с wss://gateway.discord.gg";
  } else {
    box.className = "discord-activity-box connecting";
    dot.className = "pulse-dot yellow";
    title.innerText = "⚪ СОЕДИНЕНИЕ ОСТАНОВЛЕНО";
    title.style.color = "var(--subtext)";
    desc.innerText = "Активность в Discord отключена.";
    statusLbl.innerText = "Gateway: Отключен";
  }
}

function refreshGatewayPresence() {
  if (discordWs && discordWs.readyState === WebSocket.OPEN && activeGame) {
    var startTime = Date.now() - (simSeconds * 1000);
    discordWs.send(JSON.stringify({
      op: 3,
      d: {
        since: 0,
        activities: [
          {
            name: activeGame.name,
            type: 0,
            application_id: String(activeGame.client_id),
            timestamps: {
              start: startTime
            }
          }
        ],
        status: "online",
        afk: false
      }
    }));
  }
}

function closeDiscordGateway() {
  if (discordWs) {
    try {
      if (discordWs.readyState === WebSocket.OPEN) {
        discordWs.send(JSON.stringify({
          op: 3,
          d: { since: 0, activities: [], status: "online", afk: false }
        }));
      }
      discordWs.close(1000, "User stopped");
    } catch(e){}
    discordWs = null;
  }
  if (wsHeartbeatTimer) {
    clearInterval(wsHeartbeatTimer);
    wsHeartbeatTimer = null;
  }
  wsActive = false;
  wsSeq = null;
}

// --- APP STATE & STORAGE ---
var activeMode = "quests";
var activeGame = null;
var simSeconds = 0;
var simInterval = null;
var TARGET_DURATION = 15 * 60;

function saveToken() {
  var token = sanitizeToken(document.getElementById("discordTokenInput").value);
  storage.set("eshk_discord_token", token);
}
function loadToken() {
  var saved = storage.get("eshk_discord_token", "");
  if (saved) {
    document.getElementById("discordTokenInput").value = saved;
    document.getElementById("tokenStatusBanner").innerHTML = "🔵 <b>Токен загружен.</b> Нажмите «ПРОВЕРИТЬ ТОКЕН».";
  }
}

function switchTab(mode) {
  sfxGlitch();
  activeMode = mode;
  document.getElementById('tabQuests').classList.toggle('active', mode === 'quests');
  document.getElementById('tabRemote').classList.toggle('active', mode === 'remote');
  document.getElementById('tabStandalone').classList.toggle('active', mode === 'standalone');

  document.getElementById('questsConfigCard').style.display = (mode === 'quests' ? 'block' : 'none');
  document.getElementById('remoteConfigCard').style.display = (mode === 'remote' ? 'block' : 'none');
  document.getElementById('standaloneConfigCard').style.display = (mode === 'standalone' ? 'block' : 'none');
  logEvent("Вкладка: " + mode.toUpperCase(), "act");
}

// --- SEARCH & CATEGORIES ENGINE ---
function selectCategory(cat, elem) {
  sfxGlitch();
  selectedCategory = cat;
  var chips = document.querySelectorAll(".chip");
  for (var i = 0; i < chips.length; i++) chips[i].classList.remove("active");
  if (elem) elem.classList.add("active");

  document.getElementById("gameSearchInput").value = "";
  renderGameCards("", cat);
}

function onSearchInput() {
  var q = document.getElementById("gameSearchInput").value;
  renderGameCards(q, selectedCategory);
}

function clearSearch() {
  document.getElementById("gameSearchInput").value = "";
  renderGameCards("", selectedCategory);
}

function renderGameCards(query, category) {
  var q = (query || "").toLowerCase().trim();
  var words = q ? q.split(/\s+/) : [];
  var grid = document.getElementById("gamesGrid");
  if (!grid) return;

  var results = [];
  var seenIds = {};

  // 1. User custom added games (always first)
  for (var c = 0; c < customGames.length; c++) {
    var cg = customGames[c];
    var matchCatC = (category === "all" || category === "custom");
    if (!matchCatC && !q) continue;

    var textC = (cg.name + " " + (cg.sub || "") + " " + cg.id).toLowerCase();
    var matchQC = (!q) || (words.every(function(w){ return textC.indexOf(w) !== -1; }));

    if (matchQC && (matchCatC || q)) {
      results.push({
        name: cg.name,
        id: cg.id,
        cat: "custom",
        sub: cg.sub || ("Пользовательская игра (ID: " + cg.id + ")"),
        badge: "★ МОЯ ИГРА",
        duration: cg.duration || 15,
        isCustom: true
      });
      seenIds[cg.id] = true;
    }
  }

  // 2. Curated Games & Quests
  if (category !== "custom") {
    for (var i = 0; i < CURATED_GAMES.length; i++) {
      var g = CURATED_GAMES[i];
      if (seenIds[g.id]) continue;
      var matchCat = (category === "all" || g.cat === category || (category === "quests" && g.cat === "quests"));
      if (!matchCat && !q) continue;

      var text = (g.name + " " + (g.sub || "") + " " + (g.badge || "") + " " + g.id).toLowerCase();
      var matchQ = (!q) || (words.every(function(w){ return text.indexOf(w) !== -1; }));

      if (matchQ && (matchCat || q)) {
        results.push(g);
        seenIds[g.id] = true;
      }
    }
  }

  // 3. Full 24,300+ Detectable Database
  if (category !== "custom" && fullDetectableDb && fullDetectableDb.length > 0 && (q || category === "all")) {
    for (var j = 0; j < fullDetectableDb.length; j++) {
      var fg = fullDetectableDb[j];
      if (seenIds[fg.id]) continue;

      var nameLow = fg.n.toLowerCase();
      var matchQ2 = (!q && category === "all") ? (results.length < 35) : (words.every(function(w){ return nameLow.indexOf(w) !== -1; }));

      if (matchQ2) {
        results.push({
          name: fg.n,
          id: fg.id,
          cat: "detectable",
          sub: "Discord Detectable Game (ID: " + fg.id + ")",
          badge: "🎮 VERIFIED GAME"
        });
        seenIds[fg.id] = true;
        if (results.length >= 60) break;
      }
    }
  }

  // Summary counter
  var countLbl = document.getElementById("searchResultCount");
  if (countLbl) {
    countLbl.innerText = "Найдено: " + results.length + (q ? " игр по запросу «" + q + "»" : " квестов и игр");
  }

  if (results.length === 0) {
    grid.innerHTML = '<div style="text-align: center; padding: 28px; color: var(--subtext); font-size: 12px; background: rgba(14,22,38,0.7); border-radius: 6px; border: 1px dashed var(--border);">' +
      'По запросу «' + q + '» ничего не найдено.<br>' +
      '<button class="btn btn-yellow" style="margin-top: 12px;" onclick="openAddModalWithName(\'' + q.replace(/'/g, "\\'") + '\')">+ Добавить «' + q + '» в каталог</button>' +
      '</div>';
    return;
  }

  var htmlArr = [];
  for (var k = 0; k < results.length; k++) {
    var item = results[k];
    var isCust = item.isCustom || (item.cat === "custom");
    var isQuest = (item.badge && item.badge.indexOf("QUEST") !== -1);
    var isPop = (item.badge && item.badge.indexOf("ХИТ") !== -1);
    var cardClass = "game-card" + (isCust ? " custom" : (isQuest ? " quest" : (isPop ? " popular" : "")));
    var badgeClass = "game-badge" + (isCust ? " custom-badge" : (isQuest ? " quest-badge" : (isPop ? " popular-badge" : "")));
    var btnClass = (isQuest || isCust) ? "btn btn-yellow" : (isPop ? "btn btn-primary" : "btn btn-outline");

    var safeName = item.name.replace(/"/g, "&quot;").replace(/'/g, "&#39;");
    var safeSub = (item.sub || ("Discord ID: " + item.id)).replace(/"/g, "&quot;");
    var dur = item.duration || 15;

    var deleteBtn = isCust ? '<button class="btn btn-outline btn-icon" title="Удалить игру" style="color: var(--red); border-color: var(--red);" onclick="deleteCustomGame(\'' + item.id + '\')">🗑️</button>' : '';

    htmlArr.push(
      '<div class="' + cardClass + '" data-name="' + safeName.toLowerCase() + '" data-id="' + item.id + '">' +
        '<div class="game-info">' +
          '<div class="game-name">' + safeName + '</div>' +
          '<div class="game-sub">' + safeSub + '</div>' +
          '<div class="' + badgeClass + '">' + (item.badge || "VERIFIED GAME") + '</div>' +
        '</div>' +
        '<div class="card-actions">' +
          '<button class="' + btnClass + '" onclick="launchGameByNameAndId(\'' + safeName + '\', \'' + item.id + '\', ' + dur + ')">ВЫПОЛНИТЬ</button>' +
          deleteBtn +
        '</div>' +
      '</div>'
    );
  }
  grid.innerHTML = htmlArr.join("");
}

function loadDetectableDatabase() {
  logEvent("[DB] Инициализация базы 24 300+ игр Discord...", "act");

  if (window.AndroidBridge && window.AndroidBridge.getDetectableGamesJson) {
    try {
      var raw = window.AndroidBridge.getDetectableGamesJson();
      if (raw && raw.length > 10) {
        fullDetectableDb = JSON.parse(raw);
        logEvent("[DB] База 24 300+ игр загружена (" + fullDetectableDb.length + " игр)!", "ok");
        document.getElementById("dbSourceLabel").innerText = fullDetectableDb.length + " игр в базе";
        renderGameCards("", selectedCategory);
        return;
      }
    } catch(e){
      console.warn("AndroidBridge DB load err:", e);
    }
  }

  fetch("games.json")
    .then(function(res) { return res.json(); })
    .then(function(data) {
      if (Array.isArray(data)) {
        fullDetectableDb = data;
        logEvent("[DB] База игр загружена (" + data.length + " игр)", "ok");
        document.getElementById("dbSourceLabel").innerText = data.length + " игр в базе";
        renderGameCards("", selectedCategory);
      }
    })
    ["catch"](function(err) {
      logEvent("[DB] Загружен встроенный каталог (" + CURATED_GAMES.length + " хитов)", "act");
      renderGameCards("", selectedCategory);
    });
}

// --- CONVENIENT ADD GAME WITH LIVE SUGGESTIONS (EXACT PC BEHAVIOR) ---
function onAddGameSearchInput() {
  var val = document.getElementById("newGameName").value.trim().toLowerCase();
  var drop = document.getElementById("addGameSuggestions");
  var status = document.getElementById("addGameMatchStatus");

  if (!val || val.length < 2) {
    drop.style.display = "none";
    status.innerHTML = "ℹ Введите название — ID заполнится автоматически из базы Discord";
    status.style.color = "var(--subtext)";
    return;
  }

  var words = val.split(/\s+/);
  var matches = [];
  var seen = {};

  // Check curated first
  for (var i = 0; i < CURATED_GAMES.length; i++) {
    var g = CURATED_GAMES[i];
    var nlow = g.name.toLowerCase();
    if (words.every(function(w){ return nlow.indexOf(w) !== -1; })) {
      matches.push({ name: g.name, id: g.id });
      seen[g.id] = true;
    }
  }

  // Check 24k database
  if (fullDetectableDb) {
    for (var j = 0; j < fullDetectableDb.length; j++) {
      var fg = fullDetectableDb[j];
      if (seen[fg.id]) continue;
      var fnlow = fg.n.toLowerCase();
      if (words.every(function(w){ return fnlow.indexOf(w) !== -1; })) {
        matches.push({ name: fg.n, id: fg.id });
        seen[fg.id] = true;
        if (matches.length >= 20) break;
      }
    }
  }

  if (matches.length > 0) {
    var itemsHtml = [];
    for (var m = 0; m < matches.length; m++) {
      var match = matches[m];
      var safeN = match.name.replace(/'/g, "\\'").replace(/"/g, "&quot;");
      itemsHtml.push(
        '<div class="suggestion-item" onclick="selectAddGameSuggestion(\'' + safeN + '\', \'' + match.id + '\')">' +
          '<span class="suggestion-name">★ ' + safeN + '</span>' +
          '<span class="suggestion-id">ID: ' + match.id + '</span>' +
        '</div>'
      );
    }
    drop.innerHTML = itemsHtml.join("");
    drop.style.display = "block";
    status.innerHTML = "<span style='color: var(--cyan);'>✔ Найдено в базе Discord (" + matches.length + " совпадений). Нажмите для автоподбора:</span>";
  } else {
    drop.style.display = "none";
    status.innerHTML = "<span style='color: var(--yellow);'>⚡ Пользовательская игра: введите Application ID вручную</span>";
  }
}

function selectAddGameSuggestion(name, id) {
  document.getElementById("newGameName").value = name;
  document.getElementById("newGameAppId").value = id;
  document.getElementById("addGameSuggestions").style.display = "none";
  var status = document.getElementById("addGameMatchStatus");
  status.innerHTML = "<span style='color: var(--green); font-weight: bold;'>✔ Игра найдена в базе Discord! ID: " + id + "</span>";
  sfxLaunch();
}

function saveCustomGame(launchNow) {
  var name = document.getElementById("newGameName").value.trim();
  var appId = document.getElementById("newGameAppId").value.trim();
  var dur = parseInt(document.getElementById("newGameDuration").value, 10) || 15;

  if (!name) {
    showCyberToast("⚠️ Введите название игры!", "warn");
    return;
  }
  if (!appId) {
    showCyberToast("⚠️ Укажите Discord Application ID (число)!", "warn");
    return;
  }

  customGames = customGames.filter(function(g){ return g.id !== appId; });

  customGames.unshift({
    name: name,
    id: appId,
    duration: dur,
    sub: "Пользовательская игра (ID: " + appId + ")",
    created: Date.now()
  });
  saveCustomGames();

  closeModal("addGameModal");
  showCyberToast("💾 Игра «" + name + "» сохранена в каталог!", "success");
  logEvent("Добавлена игра: " + name + " (ID: " + appId + ")", "ok");

  renderGameCards("", selectedCategory);

  if (launchNow) {
    launchGameByNameAndId(name, appId, dur);
  }
}

function deleteCustomGame(id) {
  customGames = customGames.filter(function(g){ return g.id !== id; });
  saveCustomGames();
  showCyberToast("🗑️ Игра удалена из каталога", "info");
  renderGameCards("", selectedCategory);
}

function openAddModalWithName(initialName) {
  showAddGameModal();
  if (initialName) {
    document.getElementById("newGameName").value = initialName;
    onAddGameSearchInput();
  }
}

// --- DISCORD TOKEN & USER QUESTS (@ME) ENGINE ---
function verifyToken(isSilent) {
  saveToken();
  var token = sanitizeToken(document.getElementById("discordTokenInput").value);
  if (!token) {
    if (!isSilent) {
      showCyberToast("⚠️ Сначала вставьте токен Discord!", "warn");
      logEvent("Попытка проверки с пустым полем токена", "err");
    }
    return;
  }

  var btn = document.getElementById("btnVerifyToken");
  if (btn) {
    btn.innerText = "⏳ ПРОВЕРКА...";
    btn.disabled = true;
  }
  document.getElementById("hudStatusBadge").innerText = "CONNECTING...";
  document.getElementById("tokenStatusBanner").innerHTML = "🟡 <b>Отправка запроса в Discord...</b> Пожалуйста, подождите.";
  if (!isSilent) showCyberToast("🔍 Проверка токена в Discord...", "info");
  logEvent("Отправка запроса (GET /api/v9/users/@me)...", "act");

  nativeRequest("https://discord.com/api/v9/users/@me", "GET", token, null, function(res) {
    if (btn) {
      btn.innerText = "ПРОВЕРИТЬ ТОКЕН";
      btn.disabled = false;
    }

    logEvent("Ответ Discord API: код " + res.status, res.status === 200 ? "ok" : "err");

    if (res.status === 200 && res.data && res.data.id) {
      var u = res.data;
      var tag = u.username + (u.discriminator && u.discriminator !== "0" ? "#" + u.discriminator : "");
      document.getElementById("hudStatusBadge").innerText = "ONLINE";
      document.getElementById("hudStatusBadge").className = "status-badge active";
      document.getElementById("tokenStatusBanner").innerHTML = "🟢 <b>Авторизован:</b> " + tag + " (ID: " + u.id + ") • <i>ПК не нужен, всё работает с телефона!</i>";
      document.getElementById("tokenStatusBanner").className = "token-status success";
      showCyberToast("✅ Успешный вход: " + tag, "success");
      logEvent("Успешная авторизация пользователя: " + tag, "ok");
      sfxLaunch();
      fetchUserQuests();
    } else if (res.status === 401) {
      document.getElementById("hudStatusBadge").innerText = "UNAUTHORIZED";
      document.getElementById("hudStatusBadge").className = "status-badge";
      document.getElementById("tokenStatusBanner").innerHTML = "🔴 <b>Ошибка:</b> Неверный токен (401 Unauthorized)";
      document.getElementById("tokenStatusBanner").className = "token-status error";
      showCyberToast("❌ Неверный токен Discord!", "error");
      logEvent("Токен отклонен Discord (401 Unauthorized)", "err");
      sfxGlitch();
    } else {
      document.getElementById("hudStatusBadge").innerText = "NO CONNECTION";
      document.getElementById("tokenStatusBanner").innerHTML = "⚠️ <b>Нет связи с Discord.</b> Если вы в РФ, включите VPN на телефоне (серверы Discord заблокированы РКН)!";
      document.getElementById("tokenStatusBanner").className = "token-status error";
      showCyberToast("⚠️ Нет ответа от Discord (включите VPN)!", "warn");
      logEvent("Сбой связи: " + (res.error || res.status) + " (проверьте VPN)", "err");
    }
  });
}

function fetchUserQuests(isSilent) {
  var token = sanitizeToken(document.getElementById("discordTokenInput").value);
  if (!token) return;

  if (!isSilent) showCyberToast("🔄 Загрузка квестов вашего аккаунта...", "info");
  logEvent("Запрос активных квестов (GET /api/v9/quests/@me)...", "act");

  nativeRequest("https://discord.com/api/v9/quests/@me", "GET", token, null, function(res) {
    if (res.status === 200 && res.data && res.data.quests && res.data.quests.length > 0) {
      activeUserQuests = res.data.quests;
      logEvent("Получено квестов от Discord: " + activeUserQuests.length, "ok");
      renderUserQuestsSection();
      if (!isSilent) {
        showCyberToast("🎉 Найдено активных квестов в профиле: " + activeUserQuests.length, "success");
      }
    } else {
      activeUserQuests = [];
      renderUserQuestsSection();
      logEvent("В профиле нет новых квестов, доступен общий каталог", "act");
    }
  });
}

function renderUserQuestsSection() {
  var box = document.getElementById("userQuestsBox");
  var list = document.getElementById("userQuestsList");
  if (!box || !list) return;

  if (!activeUserQuests || activeUserQuests.length === 0) {
    box.style.display = "none";
    return;
  }

  box.style.display = "block";
  var html = [];

  for (var i = 0; i < activeUserQuests.length; i++) {
    var q = activeUserQuests[i];
    var title = (q.config && q.config.messages && q.config.messages.game_title) || "Discord Quest";
    var questName = (q.config && q.config.messages && q.config.messages.quest_name) || "Задание с наградой";
    var appId = (q.config && q.config.application_id) || "";
    var isCompleted = q.user_status && q.user_status.completed_at;
    var isEnrolled = q.user_status && q.user_status.enrolled_at;

    var statusText = isCompleted ? "✅ ВЫПОЛНЕН (Награда готова!)" : (isEnrolled ? "⏳ В ПРОЦЕССЕ" : "⭐ НЕ ЗАПИСАН");
    var statusColor = isCompleted ? "var(--green)" : (isEnrolled ? "var(--yellow)" : "var(--cyan)");
    var btnText = isCompleted ? "🎁 ЗАБРАТЬ" : (isEnrolled ? "▶ ПРОДОЛЖИТЬ" : "⚡ ВЫПОЛНИТЬ");

    html.push(
      '<div style="background: rgba(10, 16, 28, 0.95); border: 1px solid var(--border); border-left: 4px solid var(--yellow); border-radius: 4px; padding: 10px; display: flex; justify-content: space-between; align-items: center; gap: 8px;">' +
        '<div style="flex: 1; min-width: 0;">' +
          '<div style="font-weight: bold; font-size: 12px; color: #FFF; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">' + title + '</div>' +
          '<div style="font-size: 10px; color: var(--subtext);">' + questName + ' (ID: ' + appId + ')</div>' +
          '<div style="font-size: 9px; font-weight: bold; color: ' + statusColor + '; margin-top: 3px;">' + statusText + '</div>' +
        '</div>' +
        '<button class="btn btn-yellow" style="padding: 8px 12px; font-size: 10px;" onclick="launchDiscordUserQuest(\'' + q.id + '\')">' + btnText + '</button>' +
      '</div>'
    );
  }

  list.innerHTML = html.join("");
}

function launchDiscordUserQuest(questId) {
  var q = activeUserQuests.find(function(x){ return x.id === questId; });
  if (!q) return;

  var token = sanitizeToken(document.getElementById("discordTokenInput").value);
  var gameTitle = (q.config && q.config.messages && q.config.messages.game_title) || "Discord Quest";
  var appId = (q.config && q.config.application_id) || questId;

  // Auto-enroll if not enrolled yet
  if (!q.user_status || !q.user_status.enrolled_at) {
    logEvent("[QUEST] Запись на квест «" + gameTitle + "»...", "act");
    nativeRequest("https://discord.com/api/v9/quests/" + questId + "/enroll", "POST", token, "{}", function(enrRes) {
      if (enrRes.status === 200) {
        logEvent("[QUEST] ✅ Успешно записан на квест «" + gameTitle + "»!", "ok");
        showCyberToast("✅ Записан на квест «" + gameTitle + "»!", "success");
        if (q.user_status) q.user_status.enrolled_at = new Date().toISOString();
        renderUserQuestsSection();
      }
    });
  }

  startQuestSimulation({
    name: gameTitle,
    client_id: appId,
    quest_id: questId,
    target_seconds: 900
  });
}

// --- GAME SPOOFING & QUEST LAUNCHER (100% STANDALONE MOBILE) ---
function launchGameByNameAndId(gameName, clientId, durMinutes) {
  if (activeGame && activeGame.client_id === clientId) {
    stopSimulation();
    return;
  }

  // Check if this game corresponds to a real active quest on the user's account
  var matchedQuest = activeUserQuests.find(function(q){
    return (q.config && String(q.config.application_id) === String(clientId)) ||
           (q.config && q.config.messages && q.config.messages.game_title && q.config.messages.game_title.toLowerCase().indexOf(gameName.toLowerCase()) !== -1);
  });

  var qId = matchedQuest ? matchedQuest.id : null;
  if (matchedQuest) {
    logEvent("[MATCH] Найдена привязка к квесту Discord: " + qId, "ok");
  }

  var targetSec = (durMinutes ? durMinutes * 60 : 900);
  startQuestSimulation({
    name: gameName,
    client_id: clientId,
    quest_id: qId,
    target_seconds: targetSec
  });
}

function startQuestSimulation(game) {
  sfxLaunch();
  activeGame = game;
  simSeconds = 0;
  TARGET_DURATION = game.target_seconds || (15 * 60);

  if (window.AndroidBridge && window.AndroidBridge.setKeepScreenOn) {
    try { window.AndroidBridge.setKeepScreenOn(true); } catch(e){}
  }

  document.getElementById("activeSimPanel").style.display = "block";
  document.getElementById("activeGameTitle").innerText = game.name;
  document.getElementById("activeTargetLabel").innerText = "ЦЕЛЬ: " + Math.round(TARGET_DURATION / 60) + " МИН";
  document.getElementById("hudStatusBadge").innerText = "RUNNING";
  document.getElementById("hudStatusBadge").className = "status-badge active";

  if (simInterval) clearInterval(simInterval);
  simInterval = setInterval(updateSimTimer, 1000);
  updateSimTimer();

  logEvent("▶ Старт активности (с телефона): " + game.name + " (ID: " + game.client_id + ")", "ok");
  showCyberToast("▶ Запущена игра: " + game.name, "success");

  // Connect Discord Gateway WebSocket to set Rich Presence "Играет в [Игра]"
  connectDiscordGateway(game);

  var token = sanitizeToken(document.getElementById("discordTokenInput").value);

  // Auto-Enroll and Heartbeats directly to Discord Quests API (NO PC NEEDED!)
  if (token && game.quest_id) {
    sendQuestHeartbeat(game.quest_id, token, false);
    if (questHeartbeatTimer) clearInterval(questHeartbeatTimer);
    questHeartbeatTimer = setInterval(function() {
      if (activeGame && activeGame.quest_id) {
        sendQuestHeartbeat(activeGame.quest_id, token, false);
        refreshGatewayPresence();
        if (simSeconds % 60 === 0) {
          fetchUserQuests(true);
        }
      }
    }, 20000);
  }
}

function sendQuestHeartbeat(questId, token, isTerminal) {
  var body = JSON.stringify({ stream_key: null, terminal: isTerminal || false });
  nativeRequest("https://discord.com/api/v9/quests/" + questId + "/heartbeat", "POST", token, body, function(r) {
    if (r.status === 200) {
      logEvent("[QUEST] Heartbeat прогресса квеста принят Discord (+20 сек)", "ok");
    } else {
      logEvent("[QUEST] Heartbeat ответ: " + r.status, "act");
    }
  });
}

function stopSimulation() {
  sfxGlitch();
  if (simInterval) clearInterval(simInterval);
  simInterval = null;
  if (questHeartbeatTimer) clearInterval(questHeartbeatTimer);
  questHeartbeatTimer = null;

  if (window.AndroidBridge && window.AndroidBridge.setKeepScreenOn) {
    try { window.AndroidBridge.setKeepScreenOn(false); } catch(e){}
  }

  var token = sanitizeToken(document.getElementById("discordTokenInput").value);
  if (activeGame && activeGame.quest_id && token && simSeconds >= TARGET_DURATION) {
    sendQuestHeartbeat(activeGame.quest_id, token, true);
    // Claim reward if eligible
    nativeRequest("https://discord.com/api/v9/quests/" + activeGame.quest_id + "/claim", "POST", token, "{\"platform\":0}", function(cr) {
      if (cr.status === 200) {
        logEvent("[QUEST] 🎉 Награда за квест успешно получена в Discord!", "ok");
        showCyberToast("🎁 Награда за квест получена в Discord!", "success");
      }
    });
  }

  var name = activeGame ? activeGame.name : "";
  activeGame = null;

  closeDiscordGateway();

  document.getElementById("activeSimPanel").style.display = "none";
  document.getElementById("hudStatusBadge").innerText = "STANDBY";
  document.getElementById("hudStatusBadge").className = "status-badge";
  showCyberToast("⏹️ Активность остановлена", "info");
  logEvent("Остановлена активность: " + name, "act");
}

function updateSimTimer() {
  simSeconds++;
  var m = Math.floor(simSeconds / 60).toString().padStart(2, '0');
  var s = (simSeconds % 60).toString().padStart(2, '0');
  document.getElementById("activeSimTimer").innerText = m + ":" + s;

  var pct = Math.min(100, (simSeconds / TARGET_DURATION) * 100);
  document.getElementById("activeProgressBar").style.width = pct + "%";

  if (simSeconds >= TARGET_DURATION) {
    sfxComplete();
    showCyberToast("🎉 КВЕСТ ВЫПОЛНЕН! 15 минут завершены!", "success");
    logEvent("🎉 КВЕСТ ПОЛНОСТЬЮ ВЫПОЛНЕН! Награда готова в Discord.", "ok");
    stopSimulation();
  }
}

// --- REMOTE PC WI-FI BRIDGE ---
function testPcConnection() {
  var ip = document.getElementById("pcIpInput").value.trim() || "192.168.1.103:8888";
  showCyberToast("📡 Проверка связи с ПК (" + ip + ")...", "info");
  logEvent("Проверка связи с ПК: http://" + ip + "/api/status", "act");

  nativeRequest("http://" + ip + "/api/status", "GET", "", null, function(res) {
    if (res.status === 200 && res.data) {
      showCyberToast("✅ Связь с ПК установлена!", "success");
      logEvent("Связь с ПК подтверждена: " + JSON.stringify(res.data), "ok");
      sfxLaunch();
    } else {
      showCyberToast("❌ Нет ответа от ПК (" + ip + "). Проверьте Wi-Fi!", "error");
      logEvent("ПК недоступен по адресу " + ip, "err");
      sfxGlitch();
    }
  });
}

function sendRemoteStop() {
  var ip = document.getElementById("pcIpInput").value.trim() || "192.168.1.103:8888";
  nativeRequest("http://" + ip + "/api/stop", "GET", "", null, function(res) {
    showCyberToast("⏹️ Сигнал остановки отправлен на ПК", "info");
    logEvent("Отправлен сигнал остановки на ПК", "act");
  });
}

function startStandaloneTimer() {
  startQuestSimulation({ name: "Таймер квеста (15 минут)", client_id: "0", target_seconds: 900 });
}

// --- MODALS ---
function showAddGameModal() {
  document.getElementById("newGameName").value = "";
  document.getElementById("newGameAppId").value = "";
  document.getElementById("addGameSuggestions").style.display = "none";
  document.getElementById("addGameMatchStatus").innerHTML = "ℹ Введите название — ID заполнится автоматически из базы Discord";
  document.getElementById("addGameModal").style.display = "flex";
}
function showTokenHelp() { document.getElementById("tokenHelpModal").style.display = "flex"; }
function closeModal(id) { document.getElementById(id).style.display = "none"; }

// Execute immediately when DOM is ready
document.addEventListener("DOMContentLoaded", function() {
  loadToken();
  loadCustomGames();
  renderGameCards("", "all");
  loadDetectableDatabase();

  if (window.AndroidBridge && window.AndroidBridge.getVideoPath) {
    try {
      var vPath = window.AndroidBridge.getVideoPath();
      if (vPath) setVideoBackground(vPath);
    } catch(e){}
  }

  logEvent("DOM готов к работе", "ok");
});

window.onload = function() {
  loadToken();
};
</script>
</body>
</html>
"""

def generate_cyber_icon(size, is_round=False):
    """Generates high contrast cyberpunk app icon for square and round launchers"""
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    bg_color = (8, 14, 24, 255)
    if is_round:
        draw.ellipse([0, 0, size - 1, size - 1], fill=bg_color, outline=(0, 240, 255, 255), width=max(2, int(size * 0.05)))
    else:
        pad = int(size * 0.04)
        draw.rectangle([pad, pad, size - 1 - pad, size - 1 - pad], fill=bg_color, outline=(0, 240, 255, 255), width=max(2, int(size * 0.05)))
        notch = int(size * 0.18)
        draw.line([pad, pad + notch, pad + notch, pad], fill=(252, 238, 10, 255), width=max(2, int(size * 0.06)))
        draw.line([size - 1 - pad - notch, size - 1 - pad, size - 1 - pad, size - 1 - pad - notch], fill=(252, 238, 10, 255), width=max(2, int(size * 0.06)))

    cx, cy = size // 2, size // 2
    w = int(size * 0.24)
    h = int(size * 0.32)
    
    draw.rectangle([cx - w, cy - h, cx - w + int(w * 0.45), cy + h], fill=(0, 240, 255, 255))
    draw.rectangle([cx - w, cy - h, cx + w, cy - h + int(h * 0.4)], fill=(252, 238, 10, 255))
    draw.rectangle([cx - w, cy - int(h * 0.16), cx + int(w * 0.75), cy + int(h * 0.16)], fill=(0, 240, 255, 255))
    draw.rectangle([cx - w, cy + h - int(h * 0.4), cx + w, cy + h], fill=(252, 238, 10, 255))
    
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def compile_clean_dex():
    """Compiles clean, 100% verified DEX bytecode with native AndroidBridge v2.7 using ECJ and Google D8"""
    build_tmp = os.path.join(BASE_DIR, ".apk_build_tmp")
    src_dir = os.path.join(build_tmp, "src")
    bin_dir = os.path.join(build_tmp, "bin")
    dex_dir = os.path.join(build_tmp, "dex")
    if os.path.exists(build_tmp):
        import shutil
        shutil.rmtree(build_tmp, ignore_errors=True)
    os.makedirs(src_dir, exist_ok=True)
    os.makedirs(bin_dir, exist_ok=True)
    os.makedirs(dex_dir, exist_ok=True)

    # Basic Android stubs for compilation
    stubs = {
        "Bundle.java": "package android.os; public class Bundle {}",
        "Looper.java": "package android.os; public class Looper { public static Looper getMainLooper() { return null; } }",
        "Handler.java": "package android.os; public class Handler { public Handler(Looper l) {} public boolean post(Runnable r) { return true; } }",
        "Toast.java": "package android.widget; public class Toast { public static final int LENGTH_SHORT = 0; public static final int LENGTH_LONG = 1; public static Toast makeText(android.content.Context c, CharSequence text, int d) { return new Toast(); } public void show() {} }",
        "JavascriptInterface.java": "package android.webkit; import java.lang.annotation.*; @Retention(RetentionPolicy.RUNTIME) @Target(ElementType.METHOD) public @interface JavascriptInterface {}",
        "View.java": "package android.view; public class View { public static final int FOCUS_DOWN = 0x00000082; public void setBackgroundColor(int color) {} public void setFocusable(boolean f) {} public void setFocusableInTouchMode(boolean f) {} public boolean requestFocus() { return true; } }",
        "Window.java": "package android.view; public class Window { public void setFlags(int a, int b) {} public void addFlags(int a) {} public void clearFlags(int a) {} public void setStatusBarColor(int c) {} }",
        "WindowManager.java": "package android.view; public class WindowManager { public static class LayoutParams { public static final int FLAG_DRAWS_SYSTEM_BAR_BACKGROUNDS = 0x80000000; public static final int FLAG_KEEP_SCREEN_ON = 0x00000080; } }",
        "ClipData.java": "package android.content; public class ClipData { public static class Item { public CharSequence getText() { return null; } } public int getItemCount() { return 0; } public Item getItemAt(int i) { return null; } }",
        "ClipboardManager.java": "package android.content; public class ClipboardManager { public boolean hasPrimaryClip() { return false; } public ClipData getPrimaryClip() { return null; } }",
        "AssetManager.java": "package android.content.res; public class AssetManager { public java.io.InputStream open(String fn) throws java.io.IOException { return null; } }",
        "Context.java": "package android.content; public class Context { public static final String CLIPBOARD_SERVICE = \"clipboard\"; public Object getSystemService(String name) { return null; } public android.content.res.AssetManager getAssets() { return null; } public java.io.File getFilesDir() { return null; } }",
        "Activity.java": "package android.app; public class Activity extends android.content.Context { protected void onCreate(android.os.Bundle b) {} protected void onPause() {} protected void onResume() {} public void setContentView(android.view.View v) {} public android.view.Window getWindow() { return null; } public void onBackPressed() {} public void finish() {} }",
        "WebSettings.java": "package android.webkit; public class WebSettings { public void setJavaScriptEnabled(boolean b) {} public void setDomStorageEnabled(boolean b) {} public void setAllowFileAccess(boolean b) {} public void setAllowContentAccess(boolean b) {} public void setDatabaseEnabled(boolean b) {} public void setCacheMode(int mode) {} public void setAllowFileAccessFromFileURLs(boolean b) {} public void setAllowUniversalAccessFromFileURLs(boolean b) {} public void setJavaScriptCanOpenWindowsAutomatically(boolean b) {} public void setMediaPlaybackRequiresUserGesture(boolean b) {} }",
        "WebResourceRequest.java": "package android.webkit; public interface WebResourceRequest { android.net.Uri getUrl(); }",
        "Uri.java": "package android.net; public abstract class Uri { public abstract String toString(); }",
        "ContentValues.java": "package android.content; public class ContentValues {}",
        "Cursor.java": "package android.database; public interface Cursor {}",
        "Intent.java": "package android.content; public class Intent {}",
        "ContentProvider.java": "package android.content; public abstract class ContentProvider { public abstract boolean onCreate(); public abstract android.database.Cursor query(android.net.Uri u, String[] p, String s, String[] a, String o); public abstract String getType(android.net.Uri u); public abstract android.net.Uri insert(android.net.Uri u, ContentValues v); public abstract int delete(android.net.Uri u, String s, String[] a); public abstract int update(android.net.Uri u, ContentValues v, String s, String[] a); }",
        "BroadcastReceiver.java": "package android.content; public abstract class BroadcastReceiver { public abstract void onReceive(Context context, Intent intent); }",
        "WebChromeClient.java": "package android.webkit; public class WebChromeClient {}",
        "WebViewClient.java": "package android.webkit; public class WebViewClient { public boolean shouldOverrideUrlLoading(WebView view, String url) { return false; } public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) { return false; } }",
        "WebView.java": "package android.webkit; public class WebView extends android.view.View { public WebView(android.content.Context ctx) {} public WebSettings getSettings() { return null; } public void setWebViewClient(WebViewClient client) {} public void setWebChromeClient(WebChromeClient client) {} public void addJavascriptInterface(Object obj, String name) {} public void loadUrl(String url) {} public void loadDataWithBaseURL(String baseUrl, String data, String mimeType, String encoding, String historyUrl) {} public void setBackgroundColor(int color) {} public boolean canGoBack() { return false; } public void goBack() {} }"
    }
    for fn, code in stubs.items():
        with open(os.path.join(src_dir, fn), "w", encoding="utf-8") as f:
            f.write(code)

    # Clean MainActivity with enhanced AndroidBridge v2.7
    with open(os.path.join(src_dir, "MainActivity.java"), "w", encoding="utf-8") as f:
        f.write('''package com.webview.myapplication;
import android.app.Activity;
import android.content.Context;
import android.content.ClipboardManager;
import android.content.ClipData;
import android.os.Bundle;
import android.os.Handler;
import android.os.Looper;
import android.view.View;
import android.view.Window;
import android.view.WindowManager;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import android.webkit.WebChromeClient;
import android.webkit.JavascriptInterface;
import android.widget.Toast;
import java.io.BufferedReader;
import java.io.ByteArrayOutputStream;
import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;

public class MainActivity extends Activity {
    private WebView mWebView;
    private final Handler mHandler = new Handler(Looper.getMainLooper());

    public static class AndroidBridge {
        private final Activity mActivity;
        private final Handler mHandler;

        public AndroidBridge(Activity act, Handler h) {
            this.mActivity = act;
            this.mHandler = h;
        }

        @JavascriptInterface
        public void showToast(final String msg) {
            mHandler.post(new Runnable() {
                @Override
                public void run() {
                    Toast.makeText(mActivity, msg, Toast.LENGTH_SHORT).show();
                }
            });
        }

        @JavascriptInterface
        public void setKeepScreenOn(final boolean keepOn) {
            mHandler.post(new Runnable() {
                @Override
                public void run() {
                    try {
                        if (mActivity != null && mActivity.getWindow() != null) {
                            if (keepOn) {
                                mActivity.getWindow().addFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
                            } else {
                                mActivity.getWindow().clearFlags(WindowManager.LayoutParams.FLAG_KEEP_SCREEN_ON);
                            }
                        }
                    } catch (Throwable ignored) {}
                }
            });
        }

        @JavascriptInterface
        public String getVideoPath() {
            try {
                File f = new File(mActivity.getFilesDir(), "fonpril.mp4");
                if (f.exists() && f.length() > 0) {
                    return "file://" + f.getAbsolutePath();
                }
            } catch (Throwable ignored) {}
            return "";
        }

        @JavascriptInterface
        public String getClipboard() {
            try {
                ClipboardManager cm = (ClipboardManager) mActivity.getSystemService(Context.CLIPBOARD_SERVICE);
                if (cm != null && cm.hasPrimaryClip() && cm.getPrimaryClip().getItemCount() > 0) {
                    ClipData.Item item = cm.getPrimaryClip().getItemAt(0);
                    if (item != null) {
                        CharSequence cs = item.getText();
                        if (cs != null) return cs.toString();
                    }
                }
            } catch (Throwable ignored) {}
            return "";
        }

        @JavascriptInterface
        public String getDetectableGamesJson() {
            try {
                InputStream is = mActivity.getAssets().open("games.json");
                ByteArrayOutputStream baos = new ByteArrayOutputStream();
                byte[] buf = new byte[8192];
                int n;
                while ((n = is.read(buf)) != -1) {
                    baos.write(buf, 0, n);
                }
                is.close();
                return baos.toString("UTF-8");
            } catch (Throwable e) {
                return "[]";
            }
        }

        @JavascriptInterface
        public String httpRequest(String urlStr, String method, String token, String jsonBody) {
            HttpURLConnection conn = null;
            try {
                URL url = new URL(urlStr);
                conn = (HttpURLConnection) url.openConnection();
                conn.setRequestMethod(method != null && !method.isEmpty() ? method.toUpperCase() : "GET");
                conn.setConnectTimeout(8000);
                conn.setReadTimeout(8000);
                conn.setRequestProperty("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36");
                conn.setRequestProperty("Content-Type", "application/json");
                conn.setRequestProperty("Accept", "*/*");
                if (token != null && !token.trim().isEmpty()) {
                    conn.setRequestProperty("Authorization", token.trim());
                }
                if ("POST".equalsIgnoreCase(method) && jsonBody != null) {
                    conn.setDoOutput(true);
                    byte[] out = jsonBody.getBytes("UTF-8");
                    conn.setFixedLengthStreamingMode(out.length);
                    OutputStream os = conn.getOutputStream();
                    os.write(out);
                    os.flush();
                    os.close();
                }
                int code = conn.getResponseCode();
                InputStream stream = (code >= 400) ? conn.getErrorStream() : conn.getInputStream();
                StringBuilder sb = new StringBuilder();
                if (stream != null) {
                    BufferedReader reader = new BufferedReader(new InputStreamReader(stream, "UTF-8"));
                    String line;
                    while ((line = reader.readLine()) != null) {
                        sb.append(line);
                    }
                    reader.close();
                }
                String resp = sb.toString().trim();
                boolean isJson = (resp.startsWith("{") && resp.endsWith("}")) || (resp.startsWith("[") && resp.endsWith("]"));
                String cleanData = isJson ? resp : ("\\"" + resp.replace("\\\\", "\\\\\\\\").replace("\\"", "\\\\\\"").replace("\\n", " ").replace("\\r", " ") + "\\"");
                return "{\\"status\\":" + code + ",\\"data\\":" + cleanData + "}";
            } catch (Exception e) {
                String errMsg = e.getMessage() != null ? e.getMessage() : "Network error";
                return "{\\"status\\":-1,\\"error\\":\\"" + errMsg.replace("\\\\", "\\\\\\\\").replace("\\"", "\\\\\\"") + "\\"}";
            } finally {
                if (conn != null) {
                    try { conn.disconnect(); } catch (Exception ignored) {}
                }
            }
        }
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        try {
            Window window = getWindow();
            if (window != null) { window.setStatusBarColor(0xFF070B14); }
        } catch (Throwable ignored) {}

        try {
            mWebView = new WebView(this);
            mWebView.setBackgroundColor(0xFF070B14);
            
            mWebView.setFocusable(true);
            mWebView.setFocusableInTouchMode(true);
            mWebView.requestFocus();

            WebSettings settings = mWebView.getSettings();
            if (settings != null) {
                settings.setJavaScriptEnabled(true);
                settings.setDomStorageEnabled(true);
                settings.setAllowFileAccess(true);
                settings.setAllowContentAccess(true);
                settings.setDatabaseEnabled(true);
                settings.setAllowFileAccessFromFileURLs(true);
                settings.setAllowUniversalAccessFromFileURLs(true);
                settings.setJavaScriptCanOpenWindowsAutomatically(true);
                settings.setMediaPlaybackRequiresUserGesture(false);
            }

            mWebView.setWebViewClient(new WebViewClient());
            mWebView.setWebChromeClient(new WebChromeClient());
            mWebView.addJavascriptInterface(new AndroidBridge(this, mHandler), "AndroidBridge");

            setContentView(mWebView);

            try {
                InputStream is = getAssets().open("eshk.html");
                ByteArrayOutputStream baos = new ByteArrayOutputStream();
                byte[] buf = new byte[8192];
                int n;
                while ((n = is.read(buf)) != -1) {
                    baos.write(buf, 0, n);
                }
                is.close();
                String html = new String(baos.toByteArray(), "UTF-8");
                mWebView.loadDataWithBaseURL("file:///android_asset/", html, "text/html", "UTF-8", null);
            } catch (Throwable e) {
                mWebView.loadUrl("file:///android_asset/eshk.html");
            }

            // Extract fonpril.mp4 in background thread to filesDir
            new Thread(new Runnable() {
                @Override
                public void run() {
                    try {
                        File dest = new File(getFilesDir(), "fonpril.mp4");
                        if (!dest.exists() || dest.length() == 0) {
                            InputStream in = getAssets().open("fonpril.mp4");
                            FileOutputStream out = new FileOutputStream(dest);
                            byte[] buf = new byte[65536];
                            int len;
                            while ((len = in.read(buf)) != -1) {
                                out.write(buf, 0, len);
                            }
                            in.close();
                            out.close();
                        }
                        final String videoUrl = "file://" + dest.getAbsolutePath();
                        mHandler.post(new Runnable() {
                            @Override
                            public void run() {
                                if (mWebView != null) {
                                    mWebView.loadUrl("javascript:setVideoBackground('" + videoUrl + "')");
                                }
                            }
                        });
                    } catch (Throwable ignored) {}
                }
            }).start();

        } catch (Throwable t) {
            t.printStackTrace();
        }
    }

    @Override
    public void onBackPressed() {
        if (mWebView != null && mWebView.canGoBack()) { mWebView.goBack(); }
        else { super.onBackPressed(); }
    }
}''')

    # InitializationProvider stub
    with open(os.path.join(src_dir, "InitializationProvider.java"), "w", encoding="utf-8") as f:
        f.write("""package androidx.startup;
import android.content.ContentProvider;
import android.content.ContentValues;
import android.net.Uri;
import android.database.Cursor;

public class InitializationProvider extends ContentProvider {
    @Override public boolean onCreate() { return true; }
    @Override public Cursor query(Uri u, String[] p, String s, String[] a, String o) { return null; }
    @Override public String getType(Uri u) { return null; }
    @Override public Uri insert(Uri u, ContentValues v) { return null; }
    @Override public int delete(Uri u, String s, String[] a) { return 0; }
    @Override public int update(Uri u, ContentValues v, String s, String[] a) { return 0; }
}""")

    # ProfileInstallReceiver stub
    with open(os.path.join(src_dir, "ProfileInstallReceiver.java"), "w", encoding="utf-8") as f:
        f.write("""package androidx.profileinstaller;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

public class ProfileInstallReceiver extends BroadcastReceiver {
    @Override public void onReceive(Context context, Intent intent) {}
}""")

    all_javas = [os.path.join(src_dir, f) for f in os.listdir(src_dir) if f.endswith(".java")]
    cmd_ecj = ["java", "-jar", os.path.join(BASE_DIR, "ecj.jar"), "-7", "-d", bin_dir] + all_javas
    res_ecj = subprocess.run(cmd_ecj, capture_output=True, text=True)
    if res_ecj.returncode != 0:
        print("ECJ compilation failed:\n", res_ecj.stderr or res_ecj.stdout)
        return None

    dex_classes = []
    for pkg in ["com", "androidx"]:
        pkg_dir = os.path.join(bin_dir, pkg)
        if os.path.exists(pkg_dir):
            for root, dirs, files in os.walk(pkg_dir):
                for file in files:
                    if file.endswith(".class"):
                        dex_classes.append(os.path.join(root, file))

    cmd_d8 = [
        "java", "-cp", os.path.join(BASE_DIR, "r8_3.jar"),
        "com.android.tools.r8.D8",
        "--min-api", "21",
        "--output", dex_dir
    ] + dex_classes
    res_d8 = subprocess.run(cmd_d8, capture_output=True, text=True)
    if res_d8.returncode != 0:
        print("D8 compilation failed:\n", res_d8.stderr or res_d8.stdout)
        return None

    final_dex = os.path.join(dex_dir, "classes.dex")
    if not os.path.exists(final_dex):
        print("classes.dex not generated by D8")
        return None

    with open(final_dex, "rb") as f:
        return f.read()

def prepare_compact_games_db():
    """Extracts compact id+name array from discord_detectable.json"""
    if not os.path.exists(DETECTABLE_SRC):
        return b"[]"
    try:
        with open(DETECTABLE_SRC, "r", encoding="utf-8") as f:
            raw = json.load(f)
        games = []
        seen_ids = set()
        for g in raw:
            gid = str(g.get("id", "")).strip()
            name = g.get("name", "").strip()
            if not gid or not name or gid in seen_ids:
                continue
            seen_ids.add(gid)
            games.append({"id": gid, "n": name})
        return json.dumps(games, separators=(',', ':'), ensure_ascii=False).encode("utf-8")
    except Exception as e:
        print(f"Warning building compact games db: {e}")
        return b"[]"

def build_apk():
    print("[1/5] Checking prerequisites and compiling clean native DEX with AndroidBridge v2.7...")
    clean_dex = compile_clean_dex()
    if not clean_dex:
        print("Failed to compile DEX.")
        return False
    print(f"  -> Clean DEX compiled successfully ({len(clean_dex)} bytes, dex 035 standard)")

    compact_games_bytes = prepare_compact_games_db()
    print(f"  -> Compact Discord detectable games DB prepared ({len(compact_games_bytes) / 1024:.1f} KB)")

    print("[2/5] Patching AndroidManifest.xml, icons, and preserving uncompressed structure...")
    in_zip = zipfile.ZipFile(TEMPLATE_APK, "r")
    out_bio = io.BytesIO()
    out_zip = zipfile.ZipFile(out_bio, "w")

    icon_map = {
        "res/9w.png": generate_cyber_icon(48, is_round=False),
        "res/zR.png": generate_cyber_icon(48, is_round=True),
        "res/yn.png": generate_cyber_icon(72, is_round=False),
        "res/8c.png": generate_cyber_icon(72, is_round=True),
        "res/FS.png": generate_cyber_icon(96, is_round=False),
        "res/wb.png": generate_cyber_icon(96, is_round=True),
        "res/FW.png": generate_cyber_icon(96, is_round=False),
        "res/RJ.png": generate_cyber_icon(144, is_round=False),
        "res/fO.png": generate_cyber_icon(144, is_round=True),
        "res/o-.png": generate_cyber_icon(192, is_round=False),
        "res/Gc.png": generate_cyber_icon(192, is_round=True),
    }

    for item in in_zip.infolist():
        filename = item.filename
        if filename.startswith("META-INF/"):
            continue
        data = in_zip.read(filename)

        target_compress_type = item.compress_type

        if filename == "classes.dex":
            data = clean_dex
            target_compress_type = zipfile.ZIP_DEFLATED

        elif filename == "resources.arsc":
            data = data.replace(b"\x0e\x0eMy Application\x00", b"\x0e\x0eEshkeri Mobile\x00")
            target_compress_type = zipfile.ZIP_STORED

        elif filename == "AndroidManifest.xml":
            data = bytearray(data)
            if len(data) > 3395 and data[3392] == 0x1E and data[3388:3392] == b"\x08\x00\x00\x10":
                data[3392] = 0x15
            data = bytes(data)

        elif filename in ["assets/eshk.html", "assets/offline.html", "assets/games.json", "assets/fonpril.mp4"]:
            continue

        elif filename in icon_map:
            data = icon_map[filename]

        zinfo = zipfile.ZipInfo(filename)
        zinfo.compress_type = target_compress_type
        out_zip.writestr(zinfo, data)

    print("[3/5] Injecting Cyberpunk Mobile Frontend, 24k Games DB & Background Video fonpril.mp4...")
    zh1 = zipfile.ZipInfo("assets/eshk.html")
    zh1.compress_type = zipfile.ZIP_DEFLATED
    out_zip.writestr(zh1, HTML_CONTENT.encode("utf-8"))

    zh2 = zipfile.ZipInfo("assets/offline.html")
    zh2.compress_type = zipfile.ZIP_DEFLATED
    out_zip.writestr(zh2, HTML_CONTENT.encode("utf-8"))

    zg = zipfile.ZipInfo("assets/games.json")
    zg.compress_type = zipfile.ZIP_DEFLATED
    out_zip.writestr(zg, compact_games_bytes)

    if os.path.exists(FONPRIL_PATH):
        print(f"  -> Packaging fonpril.mp4 ({os.path.getsize(FONPRIL_PATH)/(1024*1024):.2f} MB)...")
        zv = zipfile.ZipInfo("assets/fonpril.mp4")
        zv.compress_type = zipfile.ZIP_STORED
        with open(FONPRIL_PATH, "rb") as vf:
            out_zip.writestr(zv, vf.read())
    else:
        print("  -> Warning: fonpril.mp4 not found, skipping video asset")

    out_zip.close()

    print(f"[4/5] Writing and signing APK: {ROOT_APK}...")
    with open(ROOT_APK, "wb") as f:
        f.write(out_bio.getvalue())

    # Sign APK using uber-apk-signer (v1, v2, v3 + zipalign)
    cmd = [
        "java", "-jar", SIGNER_JAR,
        "--apks", ROOT_APK,
        "--allowResign",
        "--overwrite",
        "--verbose"
    ]
    res = subprocess.run(cmd, capture_output=True, text=True)
    if res.returncode != 0:
        print("Signing failed:\n", res.stderr or res.stdout)
        return False

    # Sync to Android_App folder
    import shutil
    shutil.copy2(ROOT_APK, OUTPUT_APK)
    print(f"  -> Synced to Android_App: {OUTPUT_APK}")

    # Sync to user's desktop folder
    if DESKTOP_APK and os.path.exists(DESKTOP_DIR):
        try:
            shutil.copy2(ROOT_APK, DESKTOP_APK)
            print(f"  -> Synced to Desktop folder: {DESKTOP_APK}")
        except Exception as e:
            print(f"  -> Warning syncing to Desktop: {e}")

    if os.path.exists(".apk_build_tmp"):
        shutil.rmtree(".apk_build_tmp", ignore_errors=True)

    print(f"[5/5] SUCCESS! Created:")
    print(f"  -> {OUTPUT_APK} ({os.path.getsize(OUTPUT_APK) / (1024*1024):.2f} MB)")
    print(f"  -> {ROOT_APK} ({os.path.getsize(ROOT_APK) / (1024*1024):.2f} MB)")
    return True

if __name__ == "__main__":
    success = build_apk()
    sys.exit(0 if success else 1)
