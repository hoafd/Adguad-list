import os
import json
import requests
import shutil
import math
import re
from datetime import datetime

# --- CẤU HÌNH ---
CONFIG_FILE = 'config/sources.json'
OUTPUT_DIR = 'output'
BACKUP_DIR = 'backup'
MAX_LINES_PER_FILE = 500_000
REPO_BASE_URL = "https://raw.githubusercontent.com/hoafd/Adguad-list/main/output/"

# 1. Dọn dẹp thư mục OUTPUT (Để tạo file mới sạch sẽ)
if os.path.exists(OUTPUT_DIR): shutil.rmtree(OUTPUT_DIR)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2. KHÔNG XÓA BACKUP, CHỈ TẠO CẤU TRÚC NẾU CHƯA CÓ
for group in ['group_a', 'group_b']:
    for category in ['whitelist', 'blocklist']:
        os.makedirs(os.path.join(BACKUP_DIR, group, category), exist_ok=True)

def url_to_filename(url):
    """
    Chuyển đổi URL thành tên file an toàn.
    Thay thế các ký tự đặc biệt (:// . / ? & =) thành gạch dưới (_)
    Ví dụ: https://example.com/list.txt -> https___example_com_list_txt.txt
    """
    # Chỉ giữ lại chữ cái, số, gạch dưới. Mọi thứ khác thành _
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', url)
    return safe_name + ".txt"

def clean_domain(text):
    line = text.strip().lower()
    if not line or line.startswith(('!', '#')): return None, False
    is_important = '$important' in line
    d = line.split('$')[0].strip()
    d = d.replace('@@', '').replace('||', '').replace('^', '')
    d = d.replace('http://', '').replace('https://', '')
    if d.startswith(('0.0.0.0', '127.0.0.1')):
        parts = d.split()
        if len(parts) >= 2: d = parts[1]
    d = d.split('/')[0].split(':')[0]
    if '.' in d: return d, is_important
    return None, False

def fetch_data(url_list, group_name, category):
    """
    Tải dữ liệu với logic: Tải Live -> Ghi Backup. Nếu lỗi -> Đọc Backup.
    Trả về Dict: { domain: is_important }
    """
    data_map = {}
    
    for url in url_list:
        filename = url_to_filename(url)
        # Đường dẫn backup phân chia rõ ràng: backup/group_a/blocklist/ten_file.txt
        backup_path = os.path.join(BACKUP_DIR, group_name, category, filename)
        
        print(f"[*] [{group_name}][{category}] Xử lý: {url[:50]}...")
        content = ""
        
        try:
            # 1. Cố gắng tải từ Internet
            r = requests.get(url, headers={'User-Agent': 'AdGuardGen/BackupMode'}, timeout=20)
            if r.status_code == 200:
                content = r.text
                # Tải thành công -> Ghi đè vào file backup ngay lập tức
                with open(backup_path, 'w', encoding='utf-8') as f: f.write(content)
            else:
                raise Exception(f"HTTP {r.status_code}")
                
        except Exception as e:
            # 2. Nếu lỗi -> Tìm file backup để cứu vãn
            print(f"   -> [!] Lỗi tải (Link chết/Mạng lỗi): {e}")
            if os.path.exists(backup_path):
                print(f"   -> [OK] Đã tìm thấy Backup cũ. Đang khôi phục dữ liệu...")
                with open(backup_path, 'r', encoding='utf-8') as f: content = f.read()
            else:
                print(f"   -> [FAIL] Không có backup. Bỏ qua nguồn này.")
        
        # 3. Phân tích nội dung (Dù là từ Live hay Backup)
        if content:
            for line in content.splitlines():
                d, imp = clean_domain(line)
                if d:
                    # Logic gộp: Nếu trùng domain, giữ lại thuộc tính important nếu có
                    current_imp = data_map.get(d, False)
                    data_map[d] = current_imp or imp
                    
    return data_map

def generate_header(title, updated_time, count, total_count, config, generated_links_text):
    lines = []
    lines.append(f"! Title: {title}")
    lines.append(f"! Updated: {updated_time}")
    lines.append(f"! Rules in this file: {count}")
    if total_count: lines.append(f"! Total Block Rules (All parts): {total_count}")
    lines.append("!")
    lines.append("! --- YOUR FILTER LINKS (Copy & Paste to AdGuard) ---")
    lines.append(generated_links_text)
    lines.append("!")
    lines.append("! --- SOURCES USED ---")
    lines.append("! [GROUP B - CORE & PRIORITY]")
    for url in config['group_b'].get('whitelist', []): lines.append(f"! - Whitelist: {url}")
    for url in config['group_b'].get('blocklist', []): lines.append(f"! - Blocklist: {url}")
    lines.append("!")
    lines.append("! [GROUP A - COMMUNITY]")
    for url in config['group_a'].get('whitelist', []): lines.append(f"! - Whitelist: {url}")
    for url in config['group_a'].get('blocklist', []): lines.append(f"! - Blocklist: {url}")
    return "\n".join(lines)

def main():
    if not os.path.exists(CONFIG_FILE): return
    with open(CONFIG_FILE) as f: config = json.load(f)

    print("\n--- BƯỚC 1: TẢI & BACKUP DỮ LIỆU ---")
    
    # Tải và phân loại vào đúng thư mục
    allow_a = fetch_data(config['group_a'].get('whitelist', []), 'group_a', 'whitelist')
    block_a = fetch_data(config['group_a'].get('blocklist', []), 'group_a', 'blocklist')
    
    allow_b = fetch_data(config['group_b'].get('whitelist', []), 'group_b', 'whitelist')
    block_b = fetch_data(config['group_b'].get('blocklist', []), 'group_b', 'blocklist')

    print("\n--- BƯỚC 2: XỬ LÝ LOGIC ---")
    
    # 1. Tổng hợp Blocklist
    # Group A: Giữ nguyên important gốc
    # Group B: Ép buộc important (True)
    final_block = {}
    for d, imp in block_a.items(): final_block[d] = imp
    for d in block_b: final_block[d] = True
    print(f"   -> Tổng Block (Raw): {len(final_block)}")

    # 2. Tổng hợp Whitelist
    final_allow = set(allow_a.keys()).union(set(allow_b.keys()))
    print(f"   -> Tổng Whitelist: {len(final_allow)}")

    # 3. Tối ưu: Xóa Block trùng Whitelist (Trừ VIP Block)
    removed_count = 0
    domains_to_remove = []
    for d in final_allow:
        if d in final_block:
            # Nếu Block này KHÔNG phải VIP -> Xóa nó đi (Whitelist thắng)
            if not final_block[d]: 
                domains_to_remove.append(d)
            # Nếu Block này LÀ VIP (Group B) -> Giữ lại (Block thắng Whitelist A)
            
    for d in domains_to_remove:
        del final_block[d]
        removed_count += 1
    print(f"   -> Đã xóa {removed_count} domain thường trùng Whitelist.")

    print("\n--- BƯỚC 3: XUẤT FILE ---")
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Tính toán parts
    sorted_block = sorted(final_block.keys())
    total_block_rules = len(sorted_block)
    total_parts = math.ceil(total_block_rules / MAX_LINES_PER_FILE)
    
    # Link Header
    links_text = []
    links_text.append(f"! > Whitelist: {REPO_BASE_URL}whitelist.txt")
    for i in range(1, total_parts + 1):
        links_text.append(f"! > Blocklist Part {i}: {REPO_BASE_URL}filter_{i:03d}.txt")
    generated_links_str = "\n".join(links_text)

    # A. Xuất Whitelist
    with open(os.path.join(OUTPUT_DIR, 'whitelist.txt'), 'w', encoding='utf-8') as f:
        header = generate_header("My Final Whitelist", timestamp, len(final_allow), None, config, generated_links_str)
        f.write(header + "\n! ---------------------------------------------------\n")
        lines = []
        for d in sorted(final_allow):
            # Check important từ nguồn (Ưu tiên B)
            imp = allow_b.get(d, False) or allow_a.get(d, False)
            rule = f"@@||{d}^" + ("$important" if imp else "")
            lines.append(rule)
        f.write('\n'.join(lines))
    print("   -> [OK] whitelist.txt")

    # B. Xuất Blocklist Parts
    block_lines = []
    for d in sorted_block:
        rule = f"||{d}^" + ("$important" if final_block[d] else "")
        block_lines.append(rule)

    for i in range(0, len(block_lines), MAX_LINES_PER_FILE):
        part_num = (i // MAX_LINES_PER_FILE) + 1
        chunk = block_lines[i : i + MAX_LINES_PER_FILE]
        filename = f"filter_{part_num:03d}.txt"
        with open(os.path.join(OUTPUT_DIR, filename), 'w', encoding='utf-8') as f:
            header = generate_header(f"My Blocklist Part {part_num}", timestamp, len(chunk), total_block_rules, config, generated_links_str)
            f.write(header + "\n! ---------------------------------------------------\n")
            f.write('\n'.join(chunk))
        print(f"   -> [OK] {filename}")

if __name__ == "__main__":
    main()
    
