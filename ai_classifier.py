import json
import re
import requests
import colorlog
import logging
from config import RULES, CAN_BO, OLLAMA_URL, OLLAMA_MODEL, LOG_FILE

# Cài đặt logger
handler = colorlog.StreamHandler()
handler.setFormatter(colorlog.ColoredFormatter(
    '%(log_color)s%(asctime)s - %(levelname)s - %(message)s'
))
file_handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))

logger = colorlog.getLogger('ai_classifier')
logger.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(file_handler)

def classify_document(doc_info):
    """
    Phân loại văn bản thành 2 tầng.
    Tầng 1: Rule-based.
    Tầng 2: Gọi Ollama AI.
    """
    text_to_search = f"{doc_info.get('trich_yeu', '')} {doc_info.get('so_ky_hieu', '')} {doc_info.get('co_quan', '')}".lower()
    
    # TẦNG 1: Rule based
    for rule_pattern, rule_category in RULES.items():
        # rule_pattern dạng: "thủ tục hành chính|nộp đảng phí|176-QĐ|văn phòng"
        keywords = rule_pattern.split('|')
        for kw in keywords:
            if kw.strip().lower() in text_to_search:
                logger.info(f"Tầng 1 match: {kw} -> {rule_category}")
                cb_info = CAN_BO.get(rule_category)
                if cb_info:
                    return {
                        "linh_vuc": rule_category,
                        "ten_linh_vuc": cb_info["ten_linh_vuc"],
                        "chu_tri": cb_info["CT"],
                        "phoi_hop": cb_info["PH"],
                        "nhan_de_biet": cb_info["NDB"],
                        "ly_do": f"Rule match: {kw}",
                        "mau_y_kien_index": 0
                    }

    # TẦNG 2: Ollama AI
    can_bo_json = json.dumps(CAN_BO, ensure_ascii=False, indent=2)
    prompt = f"""Bạn là chuyên viên văn thư Đảng ủy phường Tây Nam.
Hãy phân loại văn bản sau vào ĐÚNG 1 lĩnh vực.

Thông tin văn bản:
- Số/Ký hiệu: {doc_info.get('so_ky_hieu', '')}
- Cơ quan ban hành: {doc_info.get('co_quan', '')}
- Trích yếu: {doc_info.get('trich_yeu', '')}
- Độ khẩn: {doc_info.get('do_khan', '')}

Các lĩnh vực có thể chọn:
- kinh_te: Tài chính, ngân sách, đầu tư, doanh nghiệp, thuế
- van_hoa: Văn nghệ, thể thao, di tích, lễ hội, báo chí, du lịch
- xa_hoi: Y tế, giáo dục, chính sách, lao động, bảo hiểm

Danh sách cán bộ theo lĩnh vực:
{can_bo_json}

Trả lời CHỈ bằng JSON, không giải thích:
{{
  "linh_vuc": "kinh_te",
  "ten_linh_vuc": "Kinh tế",
  "chu_tri": "Nguyễn Văn Kinh Tế",
  "phoi_hop": ["Trần Thị Văn Hóa"],
  "nhan_de_biet": ["Lê Văn Xã Hội"],
  "ly_do": "Lý do ngắn gọn tại sao chọn lĩnh vực này",
  "mau_y_kien_index": 0
}}
"""
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "stream": False,
                "format": "json"
            },
            timeout=30
        )
        if response.status_code == 200:
            result = response.json()
            response_text = result.get('response', '{}')
            try:
                ai_data = json.loads(response_text)
                logger.info(f"Tầng 2 (AI) match: {ai_data.get('linh_vuc')}")
                return ai_data
            except json.JSONDecodeError:
                logger.error("Lỗi parse JSON từ Ollama.")
        else:
            logger.error(f"Lỗi gọi Ollama API: {response.status_code} - {response.text}")
    except Exception as e:
        logger.error(f"Lỗi kết nối Ollama: {e}")

    # Fallback
    logger.warning("Fallback về kinh_te")
    cb_info = CAN_BO["kinh_te"]
    return {
        "linh_vuc": "kinh_te",
        "ten_linh_vuc": cb_info["ten_linh_vuc"],
        "chu_tri": cb_info["CT"],
        "phoi_hop": cb_info["PH"],
        "nhan_de_biet": cb_info["NDB"],
        "ly_do": "Fallback due to error",
        "mau_y_kien_index": 0
    }
