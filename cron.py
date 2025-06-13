import requests
import time
import os
from datetime import datetime
import random

# Màu nâng cao
COLORS = [
    '\033[38;5;45m', '\033[38;5;82m', '\033[38;5;208m',
    '\033[38;5;201m', '\033[38;5;93m', '\033[38;5;226m',
    '\033[38;5;39m', '\033[38;5;196m'
]
RESET = '\033[0m'
ICONS = ['✅', '🔁', '🌀', '🚀', '📡', '⏱️', '💥', '🔗']

LINK_DIR = "links"
LINK_FILE = os.path.join(LINK_DIR, "links.txt")

def log(msg, color=None, icon=None):
    now = datetime.now().strftime("%H:%M:%S")
    color = color or random.choice(COLORS)
    icon = icon or random.choice(ICONS)
    print(f"{color}[JOONWUY - {now}] {icon} {msg}{RESET}")

def ensure_links_dir():
    if not os.path.exists(LINK_DIR):
        os.makedirs(LINK_DIR)
        log("📁 Tạo thư mục 'links/' để lưu link.", color=COLORS[4], icon="📁")

def get_links():
    ensure_links_dir()
    if os.path.exists(LINK_FILE):
        with open(LINK_FILE, "r") as f:
            links = [line.strip() for line in f if line.strip()]
            if links:
                log(f"📂 Đọc {len(links)} link từ {LINK_FILE}", color=COLORS[6], icon="📂")
                return links

    log("Nhập các link cron (phân cách bằng dấu phẩy):", color=COLORS[3], icon="📥")
    raw = input(">> ").strip()
    links = [link.strip() for link in raw.split(",") if link.strip()]
    with open(LINK_FILE, "w") as f:
        for link in links:
            f.write(link + "\n")
    log(f"💾 Đã lưu {len(links)} link vào {LINK_FILE}", color=COLORS[2], icon="💾")
    return links

def get_interval():
    while True:
        try:
            sec = float(input("Nhập thời gian lặp (giây, có thể là 0): "))
            if sec < 0:
                log("⚠️ Độ trễ không được âm!", COLORS[7], "🛑")
                continue
            return sec
        except ValueError:
            log("⚠️ Vui lòng nhập số hợp lệ!", COLORS[7], "⚠️")

def main():
    links = get_links()
    interval = get_interval()
    log(f"🚀 BẮT ĐẦU CRON JOB: {len(links)} link, mỗi {interval:.2f}s", COLORS[1], "🔥")

    while True:
        for url in links:
            try:
                response = requests.get(url)
                status = response.status_code
                if status == 200:
                    log(f"Gọi: {url} - Trạng thái: {status}", icon="✅")
                else:
                    log(f"Gọi: {url} - Lỗi HTTP: {status}", COLORS[7], "⚠️")
            except Exception as e:
                log(f"LỖI khi gọi {url}: {e}", COLORS[7], "💥")
        time.sleep(interval)

if __name__ == "__main__":
    main()
