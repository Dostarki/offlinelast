import json
import re

with open(r"c:\Users\ozan\Documents\ChatGPT\lasthoodz 2\lastzhood-main\scratch\cleaned_turkish_scan.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Files to exclude because they are false positives (English words like bot/leader)
EXCLUDE_FILES = {
    "frontend\\src\\components\\AdminBots.jsx",
    "frontend\\src\\components\\AdminPage.css",
    "frontend\\src\\components\\BossMap.jsx",
    "backend\\admin_routes.py",
    "backend\\bots.py",
    "backend\\engine.py",
    "backend\\game_settings.py",
}

for fp, hits in data.items():
    if fp in EXCLUDE_FILES:
        continue
    print(f"{fp}: {len(hits)} items")
