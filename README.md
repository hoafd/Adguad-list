# 🛡️ AdGuard Filter Generator Automation

[**Tiếng Việt**](#tiếng-việt-vietnamese) | [**English**](#english)

---

<a name="tiếng-việt-vietnamese"></a>
## 🇻🇳 Tiếng Việt (Vietnamese)

### 📋 Mục lục
* [🚀 Link sao chép nhanh](#-link-sao-chép-nhanh)
* [✨ Tính năng nổi bật](#-tính-năng-nổi-bật)
* [📁 Cấu trúc dự án](#-cấu-trúc-dự-án)
* [🛠️ Hướng dẫn cài đặt](#️-hướng-dẫn-cài-đặt)

### 🚀 Link sao chép nhanh (Raw)
*Dành cho người dùng di động: Chạm vào hộp dưới đây để sao chép link và dán vào AdGuard.*

**1. Danh sách Trắng (Whitelist - Khuyên dùng):**
```text
https://raw.githubusercontent.com/hoafd/Adguad-list/main/output/whitelist.txt
```

**2. Bộ lọc Chặn (Blocklist - Phần 1):**
```text
https://raw.githubusercontent.com/hoafd/Adguad-list/main/output/filter_001.txt
```

> [!TIP]
> Nếu bạn cần các phần tiếp theo, hãy truy cập thư mục [output](https://github.com/hoafd/Adguad-list/tree/main/output).

---

### ✨ Tính năng nổi bật
* **Tự động hóa:** Cập nhật mỗi 6 giờ, đảm bảo không bỏ lỡ các domain lừa đảo mới.
* **Đa nền tảng:** Phù hợp hoàn hảo cho AdGuard trên Android, iOS, Windows và AdGuard Home.
* **Tối ưu RAM:** Tự động chia nhỏ file giúp điện thoại cấu hình thấp không bị treo khi nạp bộ lọc.
* **An toàn:** Cơ chế whitelist thông minh tránh việc chặn nhầm các dịch vụ ngân hàng, mạng xã hội.

### 📁 Cấu trúc dự án
| Thành phần | Chi tiết |
| :--- | :--- |
| `generator.py` | "Bộ não" xử lý dữ liệu. |
| `sources.json` | Danh sách các nguồn lọc uy tín nhất. |
| `output/` | Nơi chứa các file bộ lọc đã "xuất xưởng". |

---

<a name="english"></a>
## 🇺🇸 English

### 🚀 Quick Copy Links (Raw)
*For mobile users: Tap the box below to copy and paste directly into AdGuard.*

**1. Optimized Whitelist:**
```text
https://raw.githubusercontent.com/hoafd/Adguad-list/main/output/whitelist.txt
```

**2. Optimized Blocklist (Part 1):**
```text
https://raw.githubusercontent.com/hoafd/Adguad-list/main/output/filter_001.txt
```

### ✨ Key Features
* **Auto-Sync:** Every 6 hours via GitHub Actions.
* **Mobile Friendly:** Split files for better performance on smartphones.
* **Smart Logic:** Whitelist rules always carry the `$important` flag.

---

### 🛡️ Credits
Special thanks to: **HaGeZi**, **BigDargon**, **OISD**, **ABPVN**, and the global Adblock community.

---
*Last update: 2026-02-09*
