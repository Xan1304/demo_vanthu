# ================================================
# CONFIG.PY - CẤU HÌNH HỆ THỐNG PHÂN THƯ
# Đảng ủy Phường Tây Nam
# ================================================
# ⚠️ HƯỚNG DẪN: Tìm các dòng có chữ "ĐIỀN VÀO"
# và thay thế bằng thông tin thực tế của bạn
# ================================================

# --- THÔNG TIN ĐĂNG NHẬP HỆ THỐNG ---
WEB_URL = "https://dhtn.dcs.vn/app-view/theme/admin-ex/pages/main.zul"
WEB_USERNAME = "ĐIỀN_TÊN_ĐĂNG_NHẬP"   # ⚠️ ĐIỀN VÀO
WEB_PASSWORD = "ĐIỀN_MẬT_KHẨU"         # ⚠️ ĐIỀN VÀO

# --- WHATSAPP ---
WHATSAPP_PHONE = "+84339338795"  # ⚠️ ĐIỀN VÀO
# Định dạng: +84xxxxxxxxx (không có dấu cách)

# --- AI ---
OLLAMA_MODEL = "phi3:mini"
OLLAMA_URL = "http://localhost:11434"

# --- SERVER ---
WA_SERVER_URL = "http://localhost:3000"
FLASK_PORT = 5000

# --- ĐƯỜNG DẪN FILE ---
EXCEL_FILE = r"D:\demo_phanthu\data\so_dang_ky.xlsx"
LOG_FILE = r"D:\demo_phanthu\logs\app.log"
SCREENSHOT_DIR = r"D:\demo_phanthu\screenshots"

# ================================================
# DANH SÁCH CÁN BỘ (MOCK DATA - cập nhật sau)
# Tên phải khớp CHÍNH XÁC với tên trên dhtn.dcs.vn
# ================================================
CAN_BO = {
    "kinh_te": {
        "ten_linh_vuc": "Kinh tế",
        "keywords": ["tài chính", "ngân sách", "đầu tư", "doanh nghiệp", "thuế", "kinh tế", "kế toán", "thương mại", "quản lý thị trường", "nông nghiệp", "công nghiệp"],
        "chu_tri_default": "Nguyễn Văn Kinh Tế",
        "CT": "Nguyễn Văn Kinh Tế",
        "PH": ["Trần Thị Văn Hóa"],
        "NDB": ["Lê Văn Xã Hội"]
    },
    "van_hoa": {
        "ten_linh_vuc": "Văn hóa",
        "keywords": ["văn nghệ", "thể thao", "di tích", "lễ hội", "báo chí", "truyền thông", "du lịch", "tôn giáo", "nghệ thuật", "thư viện", "tuyên truyền"],
        "chu_tri_default": "Trần Thị Văn Hóa",
        "CT": "Trần Thị Văn Hóa",
        "PH": ["Lê Văn Xã Hội"],
        "NDB": ["Nguyễn Văn Kinh Tế"]
    },
    "xa_hoi": {
        "ten_linh_vuc": "Xã hội",
        "keywords": ["y tế", "giáo dục", "chính sách", "giảm nghèo", "lao động", "việc làm", "bảo hiểm", "người có công", "trẻ em", "gia đình", "dịch bệnh", "đời sống"],
        "chu_tri_default": "Lê Văn Xã Hội",
        "CT": "Lê Văn Xã Hội",
        "PH": ["Nguyễn Văn Kinh Tế"],
        "NDB": ["Trần Thị Văn Hóa"]
    }
}

# ================================================
# QUY TẮC PHÂN LOẠI TỰ ĐỘNG (MOCK DATA)
# Định dạng: "từ_khóa|từ_khóa2": "tên_lĩnh_vực"
# ================================================
RULES = {
    "kinh tế|tài chính|doanh nghiệp|đầu tư|thuế": "kinh_te",
    "văn hóa|thể thao|du lịch|lễ hội|nghệ thuật": "van_hoa",
    "xã hội|y tế|giáo dục|lao động|bảo hiểm": "xa_hoi"
}

# ================================================
# MẪU Ý KIẾN CHUYỂN CỐ ĐỊNH (MOCK DATA)
# ================================================
MAU_Y_KIEN = [
    "Đảng bộ CQD",
    "Triển khai theo quy định",
    "Báo cáo kết quả về Văn phòng",
    "Nghiên cứu, tham mưu báo cáo Thường trực",
    "Phối hợp thực hiện theo chức năng"
]

# ================================================
# DỮ LIỆU MOCK CHO CỘT EXCEL SỔ ĐĂNG KÝ
# ================================================
EXCEL_COLUMNS = [
    "STT", "Số/Ký hiệu", "Ngày văn bản",
    "Cơ quan ban hành", "Người ký",
    "Trích yếu nội dung", "Độ mật",
    "Độ khẩn", "Số đến", "Ngày đến",
    "Chủ trì xử lý", "Ghi chú"
]

# --- MOCK WEB ---
USE_MOCK_WEB = True
MOCK_WEB_URL = "http://localhost:8080"