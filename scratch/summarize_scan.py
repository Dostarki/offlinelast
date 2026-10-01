import json
import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

with open(r"c:\Users\ozan\Documents\ChatGPT\lasthoodz 2\lastzhood-main\scratch\turkish_scan_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for filepath, hits in data.items():
    print(f"=== {filepath} ({len(hits)} matches) ===")
    for h in hits:
        print(f"  L{h['line']}: {h['content']}")
