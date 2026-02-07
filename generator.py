import os
import json
import requests
import shutil
from datetime import datetime

# --- CẤU HÌNH ---
CONFIG_FILE = 'config/sources.json'
OUTPUT_DIR = 'output'
MAX_LINES_PER_FILE = 1_500_000 

BACKUP_BLOCK_DIR = os.path.join('backup', 'block')
BACKUP_ALLOW_DIR = os.path.join('backup', 'allow')

os.makedirs(BACKUP_BLOCK_DIR, exist_ok=True)
os.makedirs(BACKUP_ALLOW_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def clean_domain(text):
    """Trích xuất domain thuần túy từ mọi định dạng"""
    text = text.strip().lower()
    if not text or text.startswith(('!', '#')):
        return None
    # Gỡ bỏ các ký tự điều hướng của AdGuard
    domain = text.replace('@@', '').replace('||', '').replace('^', '')
    # Gỡ bỏ các tùy chọn sau dấu $
    domain = domain.split('$')[0]
    # Xử lý định dạng hosts
    if domain.startswith(('0.0.0.0', '127.0.0.1')):
        parts = domain.split()
        if len(parts) >= 2: domain = parts[1]
    # Làm sạch ký tự dư thừa
    domain = domain.strip('.').split(':')[0].split('#')[0].split('/')[0]
    return domain if (domain and '.' in domain) else None

def fetch_source(name, url, save_dir):
    """Tải dữ liệu với cơ chế dự phòng Offline"""
    backup_path = os.path.join(save_dir, f"{name}.txt")
    content = ""
    print(f"[*] Đang xử lý nguồn: {name}...")
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AdGuardGenerator/1.0'}
        response = requests.get(url, headers=headers, timeout=30)
        if response.status_code == 200:
            content = response.text
            with open(backup_path, 'w', encoding='utf-8') as f:
                f.write(content)
        else:
            raise Exception(f"Lỗi HTTP {response.status_code}")
    except Exception as e:
        print(f"   -> [!] Lỗi: {e}. Đang dùng bản backup cũ.")
        if os.path.exists(backup_path):
            with open(backup_path, 'r', encoding='utf-8') as f:
                content = f.read()
        else:
            return set()

    domains = set()
    for line in content.splitlines():
        d = clean_domain(line)
        if d: domains.add(d)
    return domains

def main():
    if not os.path.exists(CONFIG_FILE):
        print(f"Lỗi: Không tìm thấy file cấu hình {CONFIG_FILE}")
        return

    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)

    raw_blocklist = set()
    allow_domains = set()
    block_sources_names = []
    allow_sources_names = []

    # --- BƯỚC 1: THU THẬP DỮ LIỆU ---
    print("\n--- BƯỚC 1: THU THẬP DỮ LIỆU ---")
    
    # Nguồn Blocklist Online
    for s in config.get('blocklist_sources', []):
        if isinstance(s, dict) and 'name' in s:
            raw_blocklist.update(fetch_source(s['name'], s['url'], BACKUP_BLOCK_DIR))
            block_sources_names.append(s['name'])
    
    # Nguồn Whitelist Online
    for s in config.get('whitelist_sources', []):
        if isinstance(s, dict) and 'name' in s:
            allow_domains.update(fetch_source(s['name'], s['url'], BACKUP_ALLOW_DIR))
            allow_sources_names.append(s['name'])

    # Nạp Local Rules (File nội bộ)
    local = config.get('local_sources', {})
    for mode, path in local.items():
        if path and os.path.exists(path):
            file_name = os.path.basename(path)
            print(f"[*] Nạp {mode} nội bộ: {path}")
            
            # Sao lưu file nội bộ
            dest_dir = BACKUP_BLOCK_DIR if mode == 'block' else BACKUP_ALLOW_DIR
            shutil.copy(path, os.path.join(dest_dir, file_name))
            
            if mode == 'block': block_sources_names.append(f"{file_name} (Local)")
            else: allow_sources_names.append(f"{file_name} (Local)")

            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    d = clean_domain(line)
                    if d:
                        if mode == 'block': raw_blocklist.add(d)
                        else: allow_domains.add(d)

    # --- BƯỚC 2: LOGIC XỬ LÝ (GIỮ NGUYÊN TRẠNG WHITELIST) ---
    print(f"\n--- BƯỚC 2: XỬ LÝ LOGIC ---")
    # Lọc blocklist: chỉ xóa nếu khớp chính xác domain có trong whitelist
    final_block_rules = sorted([f"||{d}^" for d in raw_blocklist if d not in allow_domains])
    
    # Whitelist tổng hợp: giữ nguyên tất cả domain con và cha, không tự ý lược bỏ
    whitelist_final = sorted([f"@@||{d}^$important" for d in allow_domains])

    # --- BƯỚC 3: XUẤT FILE ---
    print(f"\n--- BƯỚC 3: XUẤT FILE ---")
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # 1. Xuất whitelist.txt
    w_header = (
        f"! Title: My Optimized Whitelist\n"
        f"! Last Modified: {timestamp}\n"
        f"! Total Whitelist Rules: {len(whitelist_final)}\n"
        f"! Sources: {', '.join(allow_sources_names)}\n"
        f"! ---------------------------------------------------\n\n"
    )
    with open(os.path.join(OUTPUT_DIR, 'whitelist.txt'), 'w', encoding='utf-8') as f:
        f.write(w_header + '\n'.join(whitelist_final))
    print(f"   -> [XONG] whitelist.txt ({len(whitelist_final)} rules)")

    # 2. Xuất filter_xxx.txt
    for i in range(0, len(final_block_rules), MAX_LINES_PER_FILE):
        part_num = (i // MAX_LINES_PER_FILE) + 1
        chunk = final_block_rules[i : i + MAX_LINES_PER_FILE]
        filename = f"filter_{part_num:03d}.txt"
        
        f_header = (
            f"! Title: My Optimized Filter - Part {part_num}\n"
            f"! Last Modified: {timestamp}\n"
            f"! Rules in this part: {len(chunk)}\n"
            f"! Total Block Rules: {len(final_block_rules)}\n"
            f"! Sources: {', '.join(block_sources_names)}\n"
            f"! ---------------------------------------------------\n\n"
        )
        with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as f:
            f.write(f_header + '\n'.join(chunk))
        print(f"   -> [XONG] {filename}")

if __name__ == "__main__":
    main()
    
