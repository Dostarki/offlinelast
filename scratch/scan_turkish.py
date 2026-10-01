import os
import re
import json

ROOT = r"c:\Users\ozan\Documents\ChatGPT\lasthoodz 2\lastzhood-main"
FRONTEND_DIR = os.path.join(ROOT, "frontend", "src")
FRONTEND_PUBLIC = os.path.join(ROOT, "frontend", "public")
BACKEND_DIR = os.path.join(ROOT, "backend")

EXCLUDE_DIRS = {
    ".venv", "venv", "node_modules", "build", "dist", ".git", ".pytest_cache", "__pycache__", ".emergent"
}

TR_CHARS_PATTERN = re.compile(r'[çğıöşüÇĞİÖŞÜ]')

# Turkish common words that may not have special chars (case-insensitive)
TR_WORDS = [
    r'\baltin\b', r'\basker\b', r'\baskerler\b', r'\bkadro\b', r'\byuva\b', r'\byuvasi\b',
    r'\byukselt\b', r'\byukseltme\b', r'\bkusan\b', r'\bkusandi\b', r'\bkusandir\b', r'\benvanter\b',
    r'\batolye\b', r'\buret\b', r'\buretim\b', r'\bdonustur\b', r'\bdonusum\b', r'\btuccar\b',
    r'\bsat\b', r'\bsatis\b', r'\bpazar\b', r'\bpaketi?\b', r'\bpaketler\b', r'\bmalzeme\b',
    r'\bmalzemeler\b', r'\bparca\b', r'\bparcalar\b', r'\bkalibrasyon\b', r'\bsilah\b',
    r'\bsilahlar\b', r'\bmenzil\b', r'\bhasar\b', r'\bcan\b', r'\bzrh\b', r'\bzirh\b',
    r'\bhiz\b', r'\bhizi\b', r'\brejenerasyon\b', r'\bsarjor\b', r'\bdoldurma\b',
    r'\bdayaniklilik\b', r'\bgorevde\b', r'\bkislada\b', r'\baktif\b', r'\bpasif\b',
    r'\bgeri cek\b', r'\bgoreve cagir\b', r'\bsatin al\b', r'\bsahip\b', r'\bsahiplik\b',
    r'\byetersiz\b', r'\bgerekli\b', r'\bgereksinim\b', r'\bseviye\b', r'\bliderlik\b',
    r'\bbilgi\b', r'\bkontrol\b', r'\bkayit\b', r'\bgiris\b', r'\bcikis\b', r'\boyna\b',
    r'\bhata\b', r'\bbasari\b', r'\bbasarili\b', r'\bbasarisiz\b', r'\bsunucu\b',
    r'\bbaglanti\b', r'\bdolu\b', r'\bbos\b', r'\btuket\b', r'\biyilesme\b', r'\bcan bas\b',
    r'\bkalan\b', r'\bsure\b', r'\bdurumu?\b', r'\byenilendi\b', r'\bolduruldu\b',
    r'\boyuncu\b', r'\bdusman\b', r'\byoldas\b', r'\boyle\b', r'\bhayir\b', r'\bevet\b',
    r'\btamam\b', r'\biptal\b', r'\bkapat\b', r'\bacik\b', r'\bkapali\b', r'\byardim\b'
]
TR_WORDS_PATTERN = re.compile('|'.join(TR_WORDS), re.IGNORECASE)

def scan_file(filepath):
    hits = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception:
        try:
            with open(filepath, 'r', encoding='latin-1') as f:
                lines = f.readlines()
        except Exception:
            return hits

    for idx, line in enumerate(lines, 1):
        stripped = line.strip()
        if not stripped:
            continue
        # Skip pure comment lines if desired, but user said "ne kadar kısım varsa hepsini"
        # Let's check if there's a match
        has_tr_char = bool(TR_CHARS_PATTERN.search(line))
        has_tr_word = bool(TR_WORDS_PATTERN.search(line))
        
        if has_tr_char or has_tr_word:
            hits.append({
                'line': idx,
                'content': stripped,
                'has_char': has_tr_char,
                'has_word': has_tr_word
            })
    return hits

def main():
    results = {}

    # Directories to scan
    scan_targets = [
        (FRONTEND_DIR, ['.js', '.jsx', '.ts', '.tsx', '.json', '.css', '.html']),
        (FRONTEND_PUBLIC, ['.html', '.json']),
        (BACKEND_DIR, ['.py', '.json', '.html']),
    ]

    for base_dir, exts in scan_targets:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                if any(file.endswith(ext) for ext in exts):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, ROOT)
                    # Skip test files if wanted, or include them with note
                    hits = scan_file(full_path)
                    if hits:
                        results[rel_path] = hits

    print(f"Total files with Turkish content: {len(results)}")
    total_lines = sum(len(h) for h in results.values())
    print(f"Total lines matched: {total_lines}")

    with open(os.path.join(ROOT, "scratch", "turkish_scan_results.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
