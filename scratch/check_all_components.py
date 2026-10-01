import os
import re

COMPONENTS_DIR = r"c:\Users\ozan\Documents\ChatGPT\lasthoodz 2\lastzhood-main\frontend\src\components"

# Look for Turkish letters or Turkish words
for f in os.listdir(COMPONENTS_DIR):
    if f.endswith('.jsx'):
        p = os.path.join(COMPONENTS_DIR, f)
        with open(p, 'r', encoding='utf-8') as file:
            content = file.read()
            # check non-ascii chars
            non_ascii = set(re.findall(r'[^\x00-\x7F]', content))
            if non_ascii:
                # filter out simple bullets or symbols like •, —, ×, ↗, etc.
                tr_chars = [c for c in non_ascii if c in 'çğıöşüÇĞİÖŞÜ']
                if tr_chars:
                    print(f"{f}: has Turkish chars: {set(tr_chars)}")
