import json
import os

with open(r"c:\Users\ozan\Documents\ChatGPT\lasthoodz 2\lastzhood-main\scratch\turkish_scan_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open(r"c:\Users\ozan\Documents\ChatGPT\lasthoodz 2\lastzhood-main\scratch\scan_output.utf8.txt", "w", encoding="utf-8") as out:
    for filepath, hits in data.items():
        out.write(f"=== {filepath} ({len(hits)} matches) ===\n")
        for h in hits:
            out.write(f"  L{h['line']}: {h['content']}\n")
        out.write("\n")
