import os
import re
import json

ROOT = r"c:\Users\ozan\Documents\ChatGPT\lasthoodz 2\lastzhood-main"
FRONTEND_DIR = os.path.join(ROOT, "frontend", "src")
BACKEND_DIR = os.path.join(ROOT, "backend")

EXCLUDE_DIRS = {
    ".venv", "venv", "node_modules", "build", "dist", ".git", ".pytest_cache", "__pycache__", ".emergent"
}

TR_CHARS_PATTERN = re.compile(r'[çğıöşüÇĞİÖŞÜ]')

# Pure Turkish words that do NOT collide with common English words
TR_EXACT_WORDS = [
    r'\baltın\b', r'\baltin\b',
    r'\basker\b', r'\baskerler\b', r'\baskerlerin\b', r'\baskeri\b',
    r'\bkadro\b', r'\bkadroya\b', r'\bkadrosu\b',
    r'\byuva\b', r'\byuvası\b', r'\byuvasi\b', r'\byuvaya\b', r'\byuvadaki\b',
    r'\byükselt\b', r'\byukselt\b', r'\byükseltme\b', r'\byukseltildi\b',
    r'\bkuşan\b', r'\bkusan\b', r'\bkuşandı\b', r'\bkuşanıldı\b', r'\bkuşanmak\b',
    r'\bçıkart?\b', r'\bçıkarıldı\b',
    r'\benvanter\b', r'\batölye\b', r'\batolye\b',
    r'\büret\b', r'\buret\b', r'\büretildi\b', r'\büretimi\b', r'\büretim\b',
    r'\bdönüştür\b', r'\bdonustur\b', r'\bdönüştürüldü\b', r'\bdönüşüm\b',
    r'\btüccar\b', r'\btuccar\b', r'\btüccara\b',
    r'\bsat\b', r'\bsatıldı\b', r'\bsatılamaz\b', r'\bsatış\b',
    r'\bpazar\b', r'\bpaketler\b',
    r'\bmalzeme\b', r'\bmalzemeler\b', r'\bmalzemeleri\b', r'\bmalzemeniz\b', r'\bmalzemesine\b',
    r'\bparça\b', r'\bparçası\b', r'\bparçaları\b', r'\bparçanız\b',
    r'\bkalibrasyon\b', r'\bkartuşu\b', r'\bkartuşuna\b',
    r'\bsilah\b', r'\bsilahı\b', r'\bsilahlar\b', r'\bsilahınız\b',
    r'\bmenzil\b', r'\bmenzile\b', r'\bmenzilde\b',
    r'\bhasar\b', r'\bhasarı\b',
    r'\bzırh\b', r'\bzirh\b', r'\bzırhı\b', r'\bzırhlı\b',
    r'\bşarjör\b', r'\bsarjor\b', r'\bdoldurma\b',
    r'\bdayanıklılık\b', r'\bdayaniklilik\b',
    r'\bgörevde\b', r'\bgorevde\b', r'\bkışlada\b', r'\bkislada\b',
    r'\bgeri çek\b', r'\bgöreve çağır\b', r'\bgöreve çağrıldı\b', r'\bgörevde olabilir\b',
    r'\bsatın al\b', r'\bsahip\b', r'\bsahipsiniz\b', r'\bsahiplik\b',
    r'\byetersiz\b', r'\bgerekli\b', r'\bgereklidir\b', r'\bgereksinim\b',
    r'\bseviye\b', r'\bseviyesi\b', r'\bseviyede\b', r'\bseviyesine\b', r'\bseviyeniz\b',
    r'\bçaylak\b', r'\bdevriye\b', r'\bpiyade\b', r'\boperatör\b', r'\bmuhafız\b', r'\bmuhafızı\b',
    r'\btüket\b', r'\btuket\b',
    r'\biçecek\b', r'\biçeceği\b', r'\bstoğunuz\b',
    r'\bbakiye\b', r'\bbaşlangıç\b', r'\bbaşarıyla\b', r'\bbaşarısız\b',
    r'\bsunucu dolu\b', r'\bgiriş yapmanız gerekiyor\b', r'\basker kimliği gerekli\b',
    r'\btaktik kask\b', r'\bhücum yeleği\b', r'\bplaka taşıyıcı\b', r'\bgövde zırhı\b',
    r'\bpantolon\b', r'\bbalistik\b', r'\beldiven\b', r'\beldiveni\b', r'\bbot\b', r'\bbotu\b',
    r'\bçanta\b', r'\bçantası\b', r'\bkumaş\b', r'\bplaka\b', r'\bkayış\b', r'\bbağlantı\b'
]
TR_WORDS_PATTERN = re.compile('|'.join(TR_EXACT_WORDS), re.IGNORECASE)

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
        has_tr_char = bool(TR_CHARS_PATTERN.search(line))
        has_tr_word = bool(TR_WORDS_PATTERN.search(line))
        
        if has_tr_char or has_tr_word:
            hits.append({
                'line': idx,
                'content': stripped,
                'raw': line.rstrip('\r\n')
            })
    return hits

def main():
    results = {}
    for base_dir in [FRONTEND_DIR, BACKEND_DIR]:
        for root, dirs, files in os.walk(base_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            for file in files:
                if any(file.endswith(ext) for ext in ['.js', '.jsx', '.ts', '.tsx', '.py', '.json', '.css']):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, ROOT)
                    hits = scan_file(full_path)
                    if hits:
                        results[rel_path] = hits

    with open(os.path.join(ROOT, "scratch", "cleaned_turkish_scan.json"), "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"Cleaned scan found {len(results)} files with {sum(len(h) for h in results.values())} lines.")
    for k, v in results.items():
        print(f" - {k}: {len(v)} lines")

if __name__ == '__main__':
    main()
