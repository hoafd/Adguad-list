<a name="readme-top"></a>

<div align="center">

<h1>🛡️ Ultimate AdGuard Home Custom Filter</h1>

<p>
  <b>
    <a href="#en-intro">🇬🇧 ENGLISH</a> &nbsp;|&nbsp; <a href="#vi-intro">🇻🇳 TIẾNG VIỆT</a>
  </b>
</p>

[![Update Filter List](https://github.com/hoafd/Adguad-list/actions/workflows/update.yml/badge.svg)](https://github.com/hoafd/Adguad-list/actions/workflows/update.yml)

</div>

<br>

---

<a name="en-intro"></a>

## 🇬🇧 Introduction

This project provides a **Dual-Layer protection** system for AdGuard Home. It aggregates **1,300,000+ rules** from premium sources while solving the "Subdomain Conflict" issue by generating a high-priority Whitelist alongside optimized Blocklists.

> **Navigation:** [🚀 Installation](#en-install) • [✨ Features](#en-features) • [📂 Structure](#en-structure) • [🔧 Config & Self-Host](#en-selfhost) • [⚖️ License](#en-license)

<br>

---

<a name="en-install"></a>

### 🚀 Installation (Usage)
<div align="right">
  <a href="#readme-top">⬆️ Top</a>
</div>

To achieve 100% efficiency and avoid breaking essential apps (like FPT Play, Zalo, Banking), you **must** add both layers to your AdGuard Home.

#### 1. Layer 1: The Blocklist
* Go to **Filters** > **DNS blocklists** > **Add blocklist** > **Add a custom list**.
* **URL:**
```text
https://raw.githubusercontent.com/hoafd/Adguad-list/main/output/filter_001.txt
```

#### 2. Layer 2: The High-Priority Whitelist (Crucial)
* Go to **Filters** > **DNS allowlists** > **Add allowlist** > **Add a custom list**.
* **URL:**
```text
https://raw.githubusercontent.com/hoafd/Adguad-list/main/output/whitelist.txt
```

<br>

---

<a name="en-features"></a>

### ✨ Key Features
<div align="right">
  <a href="#readme-top">⬆️ Top</a>
</div>

* **Dual-Layer Logic:** Combines massive blocking with high-priority `@@||^` rules to ensure essential subdomains are never blocked accidentally.
* **Premium Sources Aggregation:** Merges top-tier lists from OISD, AdGuard, StevenBlack, and Vietnamese local sources.
* **Optimized for Hardware:** Automatically splits files every **1,500,000 lines** to prevent RAM exhaustion on Raspberry Pi.
* **Smart Headers:** Every generated file contains a detailed header listing the sources used and the total rule count.

<br>

---

<a name="vi-intro"></a>

<h1>🛡️ Bộ lọc tùy chỉnh tối ưu cho AdGuard Home</h1>

## 🇻🇳 Giới thiệu

Dự án này cung cấp hệ thống **Bảo vệ 2 lớp** cho AdGuard Home. Với hơn **1.300.000+ quy tắc**, hệ thống giải quyết triệt để vấn đề "Chặn nhầm Subdomain" bằng cách tạo ra song song danh sách Chặn (Blocklist) và danh sách Cho phép (Whitelist) có độ ưu tiên cao.

> **Menu nhanh:** [🚀 Cài đặt](#vi-install) • [✨ Tính năng](#vi-features) • [📂 Cấu trúc](#vi-structure) • [🔧 Tự tạo & Cấu hình](#vi-selfhost) • [⚖️ Điều khoản](#vi-license)

<br>

---

<a name="vi-install"></a>

### 🚀 Cài đặt (Hướng dẫn sử dụng)
<div align="right">
  <a href="#readme-top">⬆️ Đầu trang</a>
</div>

Để đạt hiệu quả tốt nhất và không bị lỗi các ứng dụng quan trọng, bạn **cần** thêm cả 2 lớp danh sách sau vào AdGuard Home:

#### 1. Lớp 1: Danh sách Chặn (Blocklist)
* Vào **AdGuard Home** > **Filters** > **DNS blocklists** > **Thêm danh sách chặn**.
* **Copy đường link:**
```text
https://raw.githubusercontent.com/hoafd/Adguad-list/main/output/filter_001.txt
```

#### 2. Lớp 2: Danh sách Cho phép (Whitelist - Rất quan trọng)
* Vào **AdGuard Home** > **Filters** > **DNS allowlists** > **Thêm danh sách cho phép**.
* **Copy đường link:**
```text
https://raw.githubusercontent.com/hoafd/Adguad-list/main/output/whitelist.txt
```

<br>

---

<a name="vi-features"></a>

### ✨ Tính năng & Nguồn dữ liệu
<div align="right">
  <a href="#readme-top">⬆️ Đầu trang</a>
</div>

1.  **Hệ thống 2 lớp thông minh:** Tự động tạo `whitelist.txt` với cú pháp `@@||^` giúp mở khóa các dịch vụ thiết yếu (FPT Play, Samsung TV, Zalo, MoMo...) bất chấp các bộ lọc khác có chặn gắt đến đâu.
2.  **Tổng hợp nguồn cao cấp:** Tự động gộp dữ liệu từ các nguồn uy tín: OISD, BigBlocklist, StevenBlack, AdGuard Base, ABPVN, BigDargon và HoaFD.
3.  **Bảo mật tối đa:** Tập trung chặn Malware, Phishing, Scam và các trang web cá cược lừa đảo.
4.  **Tối ưu phần cứng:** Chia nhỏ file giúp nạp danh sách mượt mà trên Raspberry Pi 3/4/5.

<br>

---

<a name="vi-structure"></a>

### 📂 Cấu trúc thư mục dự án
<div align="right">
  <a href="#readme-top">⬆️ Đầu trang</a>
</div>

```text
root/
├── .github/workflows/update.yml  # Lịch chạy tự động (mỗi 6h)
├── backup/                       # 💾 Dữ liệu dự phòng offline (Block & Allow)
├── config/sources.json           # ⚙️ CẤU HÌNH CHÍNH: Nơi quản lý các link nguồn
├── my-rules/
│   ├── allow.txt                 # Danh sách trắng cá nhân (Local Whitelist)
│   └── block.txt                 # Danh sách chặn cá nhân (Local Blocklist)
├── output/
│   ├── filter_001.txt            # Kết quả chặn đã tối ưu
│   └── whitelist.txt             # Danh sách cho phép (Priority Whitelist)
├── generator.py                  # Code Python xử lý Logic 2 lớp & Ghi Header
└── README.md                     # Tài liệu hướng dẫn
```

<br>

---

<div align="center">
  <sub>Automated by GitHub Actions • Built with ❤️ for AdGuard Home • Copyright © 2026</sub>
</div>
