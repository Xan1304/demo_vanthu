import os
import time
import random
import colorlog
import logging
from datetime import datetime
from config import WEB_URL, WEB_USERNAME, WEB_PASSWORD, SCREENSHOT_DIR, LOG_FILE

# Thử load mock web config
try:
    from config import USE_MOCK_WEB, MOCK_WEB_URL
except ImportError:
    USE_MOCK_WEB = False
    MOCK_WEB_URL = ""

from playwright.sync_api import sync_playwright

# Cài đặt logger
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s'
))
file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = colorlog.getLogger('scraper')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(file_handler)

class PlaywrightScraper:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        self.base_url = MOCK_WEB_URL if USE_MOCK_WEB else WEB_URL
        os.makedirs(SCREENSHOT_DIR, exist_ok=True)

    def start_browser(self):
        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.launch(headless=False)
            self.context = self.browser.new_context()
            self.page = self.context.new_page()
            logger.info(f"Đã khởi động Playwright browser. URL: {self.base_url}")
            
            # Đăng nhập
            self.page.goto(f"{self.base_url}/login")
            time.sleep(1)
            
            # Form login
            self.page.fill('input[name="username"]', 'test' if USE_MOCK_WEB else WEB_USERNAME)
            self.page.fill('input[name="password"]', 'test' if USE_MOCK_WEB else WEB_PASSWORD)
            self.page.click('button[type="submit"]')
            time.sleep(2)
            
        except Exception as e:
            logger.error(f"Lỗi khởi động browser: {e}")

    def get_pending_documents(self):
        try:
            logger.info("Đang lấy danh sách thư chờ...")
            # Navigate to inbox
            self.page.goto(f"{self.base_url}/inbox")
            time.sleep(random.uniform(1, 2))
            
            # Chụp ảnh
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.page.screenshot(path=os.path.join(SCREENSHOT_DIR, f"pending_{timestamp}.png"))
            
            docs = []
            rows = self.page.locator("table.van-ban-table tbody tr").all()
            for row in rows:
                if row.is_visible():
                    try:
                        doc_id_raw = row.get_attribute("id")
                        if not doc_id_raw:
                            continue
                        doc_id = doc_id_raw.replace("row-", "")
                        
                        so_ky_hieu = row.locator("td.so-ky-hieu").inner_text().strip()
                        trich_yeu = row.locator("td.trich-yeu").inner_text().strip()
                        
                        # Mock missing info for parsing
                        docs.append({
                            "doc_id": doc_id,
                            "so_ky_hieu": so_ky_hieu,
                            "trich_yeu": trich_yeu,
                            "co_quan": "",
                            "nguoi_ky": "",
                            "do_mat": "Thường",
                            "do_khan": "Thường"
                        })
                    except Exception as e:
                        logger.warning(f"Bỏ qua dòng lỗi: {e}")
            
            return docs
        except Exception as e:
            logger.error(f"Lỗi khi lấy danh sách thư: {e}")
            return []

    def get_document_detail(self, doc_id):
        try:
            logger.info(f"Đang lấy chi tiết thư {doc_id}...")
            self.page.goto(f"{self.base_url}/document/{doc_id}")
            time.sleep(random.uniform(1, 2))
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.page.screenshot(path=os.path.join(SCREENSHOT_DIR, f"detail_{doc_id}_{timestamp}.png"))
            return {"doc_id": doc_id}
        except Exception as e:
            logger.error(f"Lỗi khi lấy chi tiết thư: {e}")
            return {}

    def forward_document(self, doc_id, chu_tri, phoi_hop, nhan_de_biet, y_kien):
        try:
            logger.info(f"Đang chuyển thư {doc_id}...")
            self.page.goto(f"{self.base_url}/document/{doc_id}")
            time.sleep(1)
            
            # Click nút chuyển
            self.page.click("button.btn-chuyen")
            time.sleep(1)
            
            # Điền ý kiến
            self.page.fill("textarea.y-kien-chuyen", str(y_kien))
            
            # Tick chủ trì
            rows = self.page.locator("table.van-ban-table tbody tr").all()
            for row in rows:
                ten = row.locator("td.ten-can-bo").inner_text().strip()
                if ten == chu_tri:
                    row.locator("input.cb-chu-tri").check()
            
            # Submit
            self.page.click("button.btn-chuyen")
            time.sleep(2)
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.page.screenshot(path=os.path.join(SCREENSHOT_DIR, f"forward_{doc_id}_{timestamp}.png"))
            return True
        except Exception as e:
            logger.error(f"Lỗi khi chuyển thư: {e}")
            return False

    def close_browser(self):
        try:
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            logger.info("Đã đóng browser.")
        except Exception as e:
            logger.error(f"Lỗi khi đóng browser: {e}")
