import os
import re

UI_DIR = r"c:\Users\ozan\Documents\ChatGPT\lasthoodz 2\lastzhood-main\frontend\src\components\ui"
TR_PAT = re.compile(r'[çğıöşüÇĞİÖŞÜ]|kapat|tamam|iptal|seç|kaydet|gönder|ara', re.I)

for f in os.listdir(UI_DIR):
    if f.endswith('.jsx'):
        p = os.path.join(UI_DIR, f)
        with open(p, 'r', encoding='utf-8') as file:
            for idx, line in enumerate(file, 1):
                if TR_PAT.search(line):
                    print(f"{f}:{idx}: {line.strip()}")
