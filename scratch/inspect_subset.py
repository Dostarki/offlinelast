import json

with open(r"c:\Users\ozan\Documents\ChatGPT\lasthoodz 2\lastzhood-main\scratch\cleaned_turkish_scan.json", "r", encoding="utf-8") as f:
    data = json.load(f)

inspect_files = [
    "frontend\\src\\components\\AdminBots.jsx",
    "frontend\\src\\components\\AdminPage.css",
    "frontend\\src\\components\\BossMap.jsx",
    "backend\\admin_routes.py",
    "backend\\bots.py",
    "backend\\engine.py",
    "backend\\game_settings.py",
]

for fp in inspect_files:
    if fp in data:
        print(f"=== {fp} ===")
        for h in data[fp]:
            print(f"  L{h['line']}: {h['content']}")
